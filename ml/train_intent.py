import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

# -----------------------------
# TRAINING DATA (BALANCED)
# -----------------------------

training_data = [

    # GREETING
    ("hi", "greeting"),
    ("hello", "greeting"),
    ("hey", "greeting"),
    ("good morning", "greeting"),
    ("good evening", "greeting"),

    # REPORTING / EMERGENCY
    ("someone hacked my phone", "reporting"),
    ("my mobile is hacked", "reporting"),
    ("account hacked what to do", "reporting"),
    ("how to report cyber crime", "reporting"),
    ("where to complain about online fraud", "reporting"),
    ("someone stole my otp", "reporting"),
    ("bank fraud happened", "reporting"),

    # LAW / SECTIONS
    ("what is section 66d", "law_section"),
    ("punishment for hacking", "law_section"),
    ("it act section 43", "law_section"),
    ("ipc section for online cheating", "law_section"),
    ("what law applies for cyber fraud", "law_section"),

    # SCAM AWARENESS
    ("what is upi fraud", "scam_info"),
    ("fake loan app scam", "scam_info"),
    ("online job fraud", "scam_info"),
    ("telegram scam", "scam_info"),
    ("otp scam meaning", "scam_info"),

    # PDF QUESTIONS
    ("according to the document", "pdf_query"),
    ("based on uploaded pdf", "pdf_query"),
    ("what does the pdf say", "pdf_query"),
]

texts = [x[0] for x in training_data]
labels = [x[1] for x in training_data]

# -----------------------------
# PIPELINE
# -----------------------------

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        stop_words="english"
    )),
    ("clf", LinearSVC())
])

pipeline.fit(texts, labels)

joblib.dump(pipeline, "ml/intent_classifier.pkl")

print("✅ Intent classifier retrained successfully")
