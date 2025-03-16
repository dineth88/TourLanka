# TourLanka
A RAG based chatbot that provide information about Sri Lanka tourist destinations.

https://github.com/user-attachments/assets/34f64385-0457-41f5-8865-e82cb4bf6b85

TourLanka is a Retrieval-Augmented Generation (RAG) chatbot built to provide scholarly knowledge about Sri Lanka's top tourist destinations, their history, and importance. It uses advanced AI technologies like Huggingface Transformers, Gemini 2.0 flash LLM, and ChromaDB for efficient information retrieval and response generation.

## Features
- Provides rich historical and cultural context about Sri Lanka's top tourist destinations.
- Built using React for frontend and FastAPI for backend.
- Uses Perplexity AI for scraping context data of tourist spots.
- Embedding generation with Huggingface’s "sentence-transformers/all-MiniLM-L6-v2" model.
- Stores and retrieves knowledge in ChromaDB for efficient similarity search.
- Powered by Gemini 2.0-flash LLM for context-based query response.

## Technologies Used
- **Frontend**: React
- **Backend**: FastAPI (Python)
- **Web scraping**: Selenium
- **Embedding Model**: Huggingface "sentence-transformers/all-MiniLM-L6-v2"
- **Vector Database**: ChromaDB
- **LLM**: Gemini 2.0 flash

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js and npm

### Application Setup 

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TourLanka.git
   cd TourLanka
   
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv/Scripts/activate

3. Install required packages:
   ```bash
   pip install -r requirements.txt

4. Run scraper with custom location list:
   ```bash
   python scraper.py

5. Generate embeddings based on location_data.json:
   ```bash
   python generate_embeddings.py

6. Add Gemini API key and run the RAG application:
   ```bash
   uvicorn main:app
   cd Frontend
   npm run dev
