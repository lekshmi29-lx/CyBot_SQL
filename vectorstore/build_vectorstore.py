from database.db import SessionLocal
from database.models import (
    CyberLaw, ScamAdvisory,
    ReportingProcedure, CyberCell, LegalGuidance
)

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


FAISS_PATH = "vectorstore/faiss_index"


def load_all_data_from_db():
    db = SessionLocal()
    documents = []

    try:
        # ---------------- Cyber Laws ----------------
        for law in db.query(CyberLaw).all():
            documents.append(
                Document(
                    page_content=(
                        f"{law.act_name} {law.section} {law.title}. "
                        f"{law.description}. Punishment: {law.punishment}"
                    ),
                    metadata={"source": "cyber_laws"}
                )
            )

        # ---------------- Scam Advisories ----------------
        for scam in db.query(ScamAdvisory).all():
            documents.append(
                Document(
                    page_content=(
                        f"Scam: {scam.scam_name}. "
                        f"Method: {scam.modus_operandi}. "
                        f"Police advice: {scam.police_advice}"
                    ),
                    metadata={"source": "scam_advisories"}
                )
            )

        # ---------------- Reporting Procedures ----------------
        for rp in db.query(ReportingProcedure).all():
            documents.append(
                Document(
                    page_content=(
                        f"Crime type: {rp.crime_type}. "
                        f"Procedure: {rp.procedure}. "
                        f"Contact: {rp.contact}"
                    ),
                    metadata={"source": "reporting_procedures"}
                )
            )

        # ---------------- Legal Guidance ----------------
        for lg in db.query(LegalGuidance).all():
            documents.append(
                Document(
                    page_content=(
                        f"Crime: {lg.crime_type}. "
                        f"Laws: {lg.applicable_laws}. "
                        f"Punishment: {lg.punishment}. "
                        f"Jurisdiction: {lg.jurisdiction}"
                    ),
                    metadata={"source": "legal_guidance"}
                )
            )

        # ---------------- Cyber Cells ----------------
        for cc in db.query(CyberCell).all():
            documents.append(
                Document(
                    page_content=(
                        f"Cyber cell in {cc.district}. "
                        f"Station: {cc.station_name}. "
                        f"Phone: {cc.phone}. Email: {cc.email}"
                    ),
                    metadata={"source": "cyber_cells"}
                )
            )

    finally:
        db.close()

    return documents


def build_vectorstore():
    print("🔄 Loading data from PostgreSQL...")
    documents = load_all_data_from_db()

    if not documents:
        raise ValueError("❌ No data found in database. Cannot build FAISS index.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_PATH)

    print(f"✅ FAISS index built successfully at '{FAISS_PATH}'")


if __name__ == "__main__":
    build_vectorstore()
