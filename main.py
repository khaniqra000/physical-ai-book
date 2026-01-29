from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Frontend connection ke liye CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Qdrant Setup
client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
COLLECTION_NAME = "physical_ai_docs"

@app.get("/chat")
async def chat(query: str = Query(...)):
    try:
        # 1. Qdrant se saara upload kiya hua data nikalna
        search_results = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=10,
            with_payload=True
        )[0]
        
        # 2. Saare files ka text ek jagah jama karna (Context banana)
        all_context = ""
        for res in search_results:
            all_context += f"\n---\nSource: {res.payload.get('filename')}\n{res.payload.get('text')}"

        # 3. Gemini ko context aur sawal dena
        system_prompt = (
            "You are an expert tutor for the Physical AI course. "
            "Use the following course documentation to answer the user's question accurately. "
            "If the answer is not in the context, use your general robotics knowledge but mention it. "
            f"\n\nContext:\n{all_context}"
        )
        
        response = model.generate_content([system_prompt, f"Question: {query}"])

        return {"answer": response.text}
    except Exception as e:
        print(f"Error: {e}")
        return {"answer": "Maf kijiyega, backend mein kuch masla aa raha hai."}

@app.get("/")
def read_root():
    return {"status": "Physical AI Backend is Running!"}






app = FastAPI()
# ... baaki sara purana code ...

# Ye line lazmi honi chahiye
app = app