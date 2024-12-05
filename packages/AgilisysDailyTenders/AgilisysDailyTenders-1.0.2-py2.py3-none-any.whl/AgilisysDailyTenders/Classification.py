import spacy
import re
from . import Keywords
import gc
import site
import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

tech_docs = Keywords.tech_docs

def Preprocessing(tender):
    try:
        gc.collect()
        sites = site.getsitepackages()
        nlp = spacy.load('en_core_web_sm')
        tender = str(tender)
        tender = tender.replace("'", '"')
        tender = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', tender)).strip().lower() # Remove extra spaces and punctuation
        tender = re.sub(r'[^\x00-\x7F]+', ' ', tender)
        doc = nlp(tender)
        pos_list = ['PROPN', 'NOUN', 'ADV', 'ADJ']
        preprocessed_tender = ' '.join([d.lower_ for d in doc if d.pos_ in pos_list])
        return preprocessed_tender
    except Exception as e:
        print(f"error - {e} occured on preprocessing the tender {tender}")
        return ''

def BertEncoding(tender):
    tender = str(tender)
    model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight, effective Sentence-BERT model
    threshold=0.4
    tech_embeddings = model.encode(tech_docs)
    tender_embedding = model.encode([tender])
    similarities = cosine_similarity(tender_embedding, tech_embeddings).flatten()
    if np.any(similarities >= threshold):
        return 1
    else:
        return 0
    
def TfIdf(tender):
    tender = str(tender)
    documents = tech_docs + [tender]
    vectorizer = TfidfVectorizer()  # Create TF-IDF Vectorizer
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])    # Compute cosine similarity
    similarities = cosine_sim[0]
    threshold = 0.3  # Define threshold for classification
    for j, keyword in enumerate(tech_docs):
        if similarities[j] > threshold:
            # print(f"  - Related to tech keyword: '{keyword}' with similarity {similarities[j]:.4f}")
            return 1
    return 0

def PatternMatching(tender):
    tender_words = set(tender.split())
    related_keywords = [ keyword for keyword in tech_docs if any(word in tender_words for word in keyword.lower().split()) ]
    if related_keywords:
        # print(f"  - Related to tech keyword(s): {', '.join(related_keywords)}")
        return 1
    else:
        return 0