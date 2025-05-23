# PromoSensei: Only the Best Deals
Your smart GenAI-powered shopping assistant that retrieves and summarizes the best live promotional deals from sites like Nykaa and H&M.

---

## Features

- Real-time scraping of promotional deals (Nykaa, H&M)
- Intelligent answer generation using **RAG + LLM (Google Gemini)**
- Vector database (FAISS) for efficient retrieval
- Simple UI via **Streamlit** 

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sim01web/promosensei.git
cd promosensei
```

### 2. Create a config.py inside the root directory that will contain your Gemini API Key:
```bash
GEMINI_API_KEY = "your_api_key"
```
### 3. Install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the ingest_to_vector_db.py to scrape the ecommerce websites for offers and build the Vector DB:
```bash
python ingest_to_vector_db.py
```
### 5. Launch the streamlit app:
```bash
streamlit run chatbot_ui.py
```
#### Some input and output screenshots:

![image](https://github.com/user-attachments/assets/c3d2aadc-cb65-4ccc-a910-6c32eefba3be)

![image](https://github.com/user-attachments/assets/f3c0ee89-c06c-4c8b-a466-1444f34cce04)

![image](https://github.com/user-attachments/assets/7038421e-b601-4a9c-9893-e7519667abf8)



