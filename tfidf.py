import fitz  # PyMuPDF
from docx import Document
import spacy
from summa import keywords as textrank_keywords
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Load spaCy model
nlp = spacy.load("xx_sent_ud_sm")

# ==== 1. Load document ====
def load_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    return " ".join([page.get_text() for page in doc])

def load_text_from_docx(filepath):
    doc = Document(filepath)
    return " ".join([para.text for para in doc.paragraphs])

# ==== 2. spaCy tokenizer ====
def spacy_tokenizer(text):
    doc = nlp(text.lower())
    return [token.text for token in doc if not token.is_stop and not token.is_punct and not token.is_space]

# ==== 3. TextRank keywords ====
def get_textrank_keywords(text, language='indonesian', top_n=10):
    return textrank_keywords.keywords(text, language=language, split=True, scores=True)[:top_n]

# ==== 4. TF-IDF keywords ====
def get_tfidf_keywords(tokens, top_n=10):
    def identity(x): return x
    vectorizer = TfidfVectorizer(
        tokenizer=identity,
        preprocessor=None,
        token_pattern=None,
        lowercase=False
    )
    tfidf_matrix = vectorizer.fit_transform([tokens])
    df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
    return df.T[0].sort_values(ascending=False).head(top_n)

# ==== 5. Word Cloud Visualization ====
def show_wordcloud(freq_dict, title="Word Cloud"):
    wc = WordCloud(width=800, height=400, background_color='white')
    wc.generate_from_frequencies(freq_dict)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.show()

# ==== 6. Main logic ====

# --- Load your file (choose one) ---
# text = load_text_from_pdf("your_file.pdf")
text = load_text_from_docx("your_file.docx")

# --- Tokenize ---
tokens = spacy_tokenizer(text)

# --- TF-IDF Keywords ---
tfidf_keywords = get_tfidf_keywords(tokens, top_n=15)

# --- TextRank Keywords ---
textrank_keywords_list = get_textrank_keywords(" ".join(tokens), language='indonesian', top_n=15)
textrank_dict = dict(textrank_keywords_list)

# --- Show word clouds ---
show_wordcloud(tfidf_keywords.to_dict(), title="🌟 TF-IDF Keywords")
show_wordcloud(textrank_dict, title="🧠 TextRank Keywords")



#_----- all in a succession
import fitz  # PyMuPDF
import glob
import os
import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# === 1. Load spaCy Indonesian tokenizer ===
nlp = spacy.load("xx_sent_ud_sm")

# === 2. Extract text from PDF ===
def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    return " ".join([page.get_text() for page in doc])

# === 3. Tokenize text ===
def tokenize_indonesian(text):
    doc = nlp(text.lower())
    return [
        token.text for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]

# === 4. Load multiple PDFs ===
def load_tokens_from_pdfs(folder_path):
    all_tokens = []
    docwise_tokens = []
    filepaths = glob.glob(os.path.join(folder_path, "*.pdf"))

    for path in filepaths:
        print(f"📄 Reading: {os.path.basename(path)}")
        text = extract_text_from_pdf(path)
        tokens = tokenize_indonesian(text)
        all_tokens.extend(tokens)
        docwise_tokens.append(tokens)
    return all_tokens, docwise_tokens, filepaths

# === 5. TF-IDF computation ===
def get_tfidf_keywords(docs_tokens, top_n=20):
    def identity(x): return x
    vectorizer = TfidfVectorizer(
        tokenizer=identity,
        preprocessor=None,
        token_pattern=None,
        lowercase=False
    )
    tfidf_matrix = vectorizer.fit_transform(docs_tokens)
    feature_names = vectorizer.get_feature_names_out()
    df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
    # Sum across all docs to get global importance
    return df.sum(axis=0).sort_values(ascending=False).head(top_n)

# === 6. Show word cloud ===
def show_wordcloud(freq_dict, title):
    wc = WordCloud(width=800, height=400, background_color='white')
    wc.generate_from_frequencies(freq_dict)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.show()

# === 7. MAIN RUN ===
pdf_folder = "your_pdf_folder"  # Replace with your folder path
corpus_tokens, per_doc_tokens, pdf_files = load_tokens_from_pdfs(pdf_folder)

# === 8. Most common words (by frequency) ===
freq_counter = Counter(corpus_tokens)
most_common_words = freq_counter.most_common(20)

print("\n🔢 Most Frequent Words:")
for word, count in most_common_words:
    print(f"{word}: {count}")

# === 9. TF-IDF Important Words ===
tfidf_keywords = get_tfidf_keywords(per_doc_tokens, top_n=20)

print("\n🌟 Most Important (TF-IDF) Words:")
print(tfidf_keywords)

# === 10. Word Clouds ===
show_wordcloud(dict(most_common_words), title="🔢 Most Common Words")
show_wordcloud(tfidf_keywords.to_dict(), title="🌟 Most Important (TF-IDF) Words")




