import os
import signal
import sys
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

def signal_handler(sig, frame):
    print('\n Thank you.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_rag_prompt(query, context):
    escaped = context.replace("'", "").replace('""', "").replace("\n", " ")
    prompt = ("""
                You are a helpful and informative bot that provides historical 
                data about the location that the user inputs. The historical data you 
                have been provided may contain reference numbers along with the text. 
                Remove them and pass the output. 

                If the answer for a certain prompt is not available in the context, then process the answer by yourself knowledge. 
                You are providing answers for tourists. Make the content more attractive 
                for them to read. Ensure to respond in complete sentences, be comprehensive, 
                and structure the response properly. Always state the whole answer as much as possible. 

                Also, remove unnecessary symbols from the answer. You have provided data 
                in JSON format as {{'location': 'location name', 'historical data': 'historical context'}}.

                And user entering question. 
                QUESTION: '{query}'
                CONTEXT: '{context}'
                Provide answer by going through context
                ANSWER: 
            """).format(query=query, context=context)
    
    return prompt

def get_relevant_context_from_db(query):
    context = ""
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device':'cpu'})
    vector_db = Chroma(persist_directory="./chroma_db_nccn", embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=16) # k for the number of chunks output
    for result in search_results:
        context += result.page_content + "\n"
    return context

def generate_answer(prompt):
    genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model_name='gemini-2.0-flash')
    answer = model.generate_content(prompt)
    return answer.text

app=FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main(query: str):
    print("------------------------------------------------------------------------------------")
    print(f"User Query: {query}")

    context = get_relevant_context_from_db(query)
    prompt = generate_rag_prompt(query=query, context=context)
    answer = generate_answer(prompt=prompt)

    print(f"Bot Answer: {answer}")
    return JSONResponse(content={"response": answer})