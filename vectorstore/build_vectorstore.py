from database.db import SessionLocal
from database.models import (
    CyberLaw, ScamAdvisory,
    ReportingProcedure, CyberCell, LegalGuidance
)

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


def load_all_data_from_db():
    db = SessionLocal()
    texts = []

    for law in db.query(CyberLaw).all():
        texts.append(
            f"{law.act_name} {law.section} {law.title}. "
            f"{law.description}. Punishment: {law.punishment}"
        )

    for scam in db.query(ScamAdvisory).all():
        texts.append(
            f"Scam: {scam.scam_name}. "
            f"Method: {scam.modus_operandi}. "
            f"Police advice: {scam.police_advice}"
        )

    for rp in db.query(ReportingProcedure).all():
        texts.append(
            f"Crime type: {rp.crime_type}. "
            f"Procedure: {rp.procedure}. "
            f"Contact: {rp.contact}"
        )

    for lg in db.query(LegalGuidance).all():
        texts.append(
            f"Crime: {lg.crime_type}. "
            f"Laws: {lg.applicable_laws}. "
            f"Punishment: {lg.punishment}. "
            f"Jurisdiction: {lg.jurisdiction}"
        )

    for cc in db.query(CyberCell).all():
        texts.append(
            f"Cyber cell in {cc.district}. "
            f"Station: {cc.station_name}. "
            f"Phone: {cc.phone}. Email: {cc.email}"
        )

    db.close()
    return texts


def build_vectorstore():
    print("🔄 Loading data from PostgreSQL...")
    texts = load_all_data_from_db()

    documents = [Document(page_content=t) for t in texts]

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("vectorstore/faiss_index")

    print("✅ FAISS index built from SQL")


if __name__ == "__main__":
    build_vectorstore()
