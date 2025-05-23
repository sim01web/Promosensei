import faiss
import pickle
import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer

import google.generativeai as genai
from config import GEMINI_API_KEY  # or use os.getenv("GEMINI_API_KEY")

# Setup
genai.configure(api_key=GEMINI_API_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')

VECTOR_DIM = 384
DB_PATH = "faiss_index"

def load_vector_db():
    index = faiss.read_index(f"{DB_PATH}/offers.index")
    with open(f"{DB_PATH}/offers_meta.pkl", "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def retrieve_offers(query: str, top_k: int = 5) -> List[Dict]:
    index, metadata = load_vector_db()
    query_embedding = model.encode([query])
    scores, indices = index.search(query_embedding, top_k)
    return [metadata[i] for i in indices[0] if i < len(metadata)]

def generate_response_with_gemini(query: str, offers: List[Dict]) -> str:
    context = "\n\n".join([
        f"- {offer['title']}\n  Brand: {offer['brand']}, Price: {offer['price']}, MRP: {offer['mrp']}, Discount: {offer['discount']}, Link: {offer['link']}"
        for offer in offers
    ])

    prompt = (
        f"You are a smart deal assistant. Based on the following user query:\n"
        f"'{query}'\n\n"
        f"Here are the available promotional offers:\n{context}\n\n"
        f"Please generate a clear, concise summary of the deals found in the context and also provide respective links for each deal found. Don't give additional offers and stick to the products asked by the user."
    )

    gemini = genai.GenerativeModel("gemini-2.0-flash")
    response = gemini.generate_content(prompt, generation_config={"temperature": 0})
    return response.text.strip()

if __name__ == "__main__":
    user_query = input("Enter your query (e.g., 'any haircare discounts?'):\n> ")
    offers = retrieve_offers(user_query)

    if not offers:
        print("No matching offers found.")
    else:
        summary = generate_response_with_gemini(user_query, offers)
        print("\nPromoSensei's Response:\n")
        print(summary)
