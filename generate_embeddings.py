import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Load the JSON file correctly
with open("location_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Ensure it's parsed into a Python list/dict

# Ensure data is a list of dictionaries
if isinstance(data, str):  # Fix if JSON was loaded as a string
    data = json.loads(data)

# Verify correct JSON format
print(type(data))  # Should be <class 'list'>
print(data[0])  # Print first item to verify structure

# Process JSON data into documents
docs = []
for item in data:
    try:
        docs.append(Document(
            page_content=json.dumps(item["historicalData"], indent=2),  # Convert nested dict to string
            metadata={"location": item["location"]}
        ))
    except KeyError as e:
        print(f"Missing key: {e} in item: {item}")

# Split the text into smaller chunks for embedding
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(docs)

# Create vector database
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db_nccn")

print("Total embedded documents:", vectorstore._collection.count())
