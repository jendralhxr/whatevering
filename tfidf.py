# Required libraries
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# STEP 1: Load spaCy multilingual tokenizer (includes Indonesian)
# Install if needed: python -m spacy download xx_sent_ud_sm
nlp = spacy.load("xx_sent_ud_sm")

# STEP 2: Sample Indonesian corpus
corpus = [
    "Pemanfaatan limbah organik menjadi pupuk kompos sangat penting bagi pertanian berkelanjutan.",
    "Teknologi pengolahan air limbah terus berkembang untuk menjaga lingkungan.",
    "Penggunaan energi terbarukan seperti tenaga surya dan angin semakin meningkat di Indonesia."
]

# STEP 3: Custom tokenizer function using spaCy
def spacy_tokenizer(text):
    doc = nlp(text.lower())  # lowercase and tokenize
    tokens = [
        token.text for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return tokens

# STEP 4: Adapter so scikit-learn can use our tokenizer
def identity_tokenizer(text):
    return text

# STEP 5: Preprocess corpus with spaCy tokenizer
tokenized_corpus = [spacy_tokenizer(doc) for doc in corpus]

# STEP 6: TF-IDF with pre-tokenized input
vectorizer = TfidfVectorizer(
    tokenizer=identity_tokenizer,  # bypass default tokenizer
    preprocessor=None,
    token_pattern=None,
    lowercase=False,               # already handled
)

tfidf_matrix = vectorizer.fit_transform(tokenized_corpus)
feature_names = vectorizer.get_feature_names_out()

# Convert to DataFrame
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

# Sum across all docs to get global importance
global_importance = df_tfidf.sum(axis=0).sort_values(ascending=False)

print("\n Most Important (TF-IDF) Words:")
print(global_importance.head(10))

#---- PDF
import fitz  # PyMuPDF
def extract_pdf_words(filepath):
    doc = fitz.open(filepath)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    # Tokenize and clean with spaCy
    tokens = [
        token.text for token in nlp(full_text.lower())
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return tokens

tokens = extract_pdf_words("your_file.pdf")

#------ DOC/DOCX
from docx import Document
def extract_docx_words(filepath):
    doc = Document(filepath)
    full_text = " ".join([para.text for para in doc.paragraphs])
    tokens = [
        token.text for token in nlp(full_text.lower())
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return tokens

tokens = extract_docx_words("your_file.docx")



#---------- textrank
import fitz  # for PDF
from docx import Document  # for DOCX
import spacy
from summa import keywords as textrank_keywords

# Load spaCy multilingual model
nlp = spacy.load("xx_sent_ud_sm")

# === 1. Load text from PDF ===
def load_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    return " ".join([page.get_text() for page in doc])

# === 2. Load text from DOCX ===
def load_text_from_docx(filepath):
    doc = Document(filepath)
    return " ".join([para.text for para in doc.paragraphs])

# === 3. Run TextRank on text ===
def extract_keywords_textrank(text, language='indonesian', num_keywords=10):
    kw = textrank_keywords.keywords(text, language=language, split=True, scores=True)
    return kw[:num_keywords]

# === 4. Choose your source ===
# text = load_text_from_pdf("your_file.pdf")
text = load_text_from_docx("your_file.docx")

# === 5. Extract keywords using TextRank ===
keywords_ranked = extract_keywords_textrank(text)
print("🔑 Top Keywords (TextRank):")
for word, score in keywords_ranked:
    print(f"{word} ({score:.4f})")

