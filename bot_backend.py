import joblib
import fitz
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from sentence_transformers import CrossEncoder

# Intent model
intent_classifier = joblib.load("ml/intent_classifier.pkl")

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS (BUILT FROM SQL)
vectorstore = FAISS.load_local(
    "vectorstore/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# LLM
llm = ChatOllama(model="llama3:8b", temperature=0.3)

# Re-ranker
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# PDF memory
pdf_vectorstores = {}


def predict_intent(query):
    return intent_classifier.predict([query])[0]


def process_pdf(pdf_id, file_path):
    doc = fitz.open(file_path)
    text = "".join([p.get_text() for p in doc])

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )

    docs = [
        Document(page_content=c, metadata={"source": "pdf"})
        for c in splitter.split_text(text)
    ]

    pdf_vectorstores[pdf_id] = FAISS.from_documents(docs, embeddings)


def remove_pdf_from_memory(pdf_id):
    pdf_vectorstores.pop(pdf_id, None)


def get_bot_response(user_question, has_pdf=False, pdf_id=None):
    intent = predict_intent(user_question)

    # =====================================================
    # 1️⃣ GREETING (NO LLM, NO FAISS)
    # =====================================================
    if intent == "greeting":
        return (
            "<p>Hello! 👋</p>"
            "<p>I’m <strong>Cy-Bot</strong>, your Kerala Cyber Law Assistant.</p>"
            "<p>How can I help you today regarding cybercrime or digital safety?</p>"
        )

    # =====================================================
    # 2️⃣ REPORTING / EMERGENCY INTENT (DIRECT RESPONSE)
    # =====================================================
    if intent == "reporting":
        return (
            "<p><strong>Based on Kerala cybercrime reporting procedures:</strong></p>"
            "<p>If your phone or account has been hacked:</p>"
            "<ul>"
            "<li>Immediately disconnect the device from the internet</li>"
            "<li>Change passwords for email, bank, and social media</li>"
            "<li>Enable two-factor authentication</li>"
            "<li>Call <strong>1930</strong> to report cyber fraud</li>"
            "<li>File a complaint at "
            "<a href='https://cybercrime.gov.in' target='_blank'>cybercrime.gov.in</a>"
            "</li>"
            "</ul>"
        )

    # =====================================================
    # 3️⃣ NORMAL RAG FLOW (LAW / SCAM / PDF QUESTIONS)
    # =====================================================
    docs = retriever.invoke(user_question)

    # Add PDF context if available
    if has_pdf and pdf_id in pdf_vectorstores:
        pdf_retriever = pdf_vectorstores[pdf_id].as_retriever(
            search_kwargs={"k": 3}
        )
        pdf_docs = pdf_retriever.invoke(user_question)
        docs = docs + pdf_docs

    # =====================================================
    # 4️⃣ NO CONTEXT FOUND → SAFE RESPONSE
    # =====================================================
    if not docs:
        return (
            "<p><strong>I couldn’t find specific information</strong> about this "
            "in Kerala’s cyber laws or your uploaded documents.</p>"
            "<p>You may try rephrasing your question or ask about reporting "
            "procedures, cyber scams, or legal sections.</p>"
        )

    # =====================================================
    # 5️⃣ RE-RANKING (QUALITY CONTROL)
    # =====================================================
    pairs = [[user_question, d.page_content] for d in docs]
    scores = reranker.predict(pairs)

    docs = [
        d for d, _ in sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )[:3]
    ]

    context = "\n\n".join(d.page_content for d in docs)

    # =====================================================
    # 6️⃣ CLEAN SYSTEM PROMPT (NO INTRODUCTION LOOP)
    # =====================================================
    prompt = f"""
You are Cy-Bot, a Kerala Cyber Law Assistant.

Rules:
1. Answer ONLY using the context below.
2. If information is from Kerala cyber laws, say:
   "Based on Kerala's cyber laws..."
3. If information is from uploaded PDF, say:
   "According to the document you provided..."
4. If both are used, mention both.
5. Do NOT introduce yourself.
6. Use simple, clear language.
7. Format response in HTML using <p>, <ul>, <li>, <strong>.

Context:
{context}

Question:
{user_question}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content.strip()
