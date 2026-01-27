import os
import glob
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

# Qdrant Connect
client = QdrantClient(
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "physical_ai_docs"

def start_ingestion():
    print("🚀 Qdrant connect ho raha hai...")
    
    # 1. Naya collection banana (Size 4 rakha hai testing ke liye)
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=4, distance=Distance.COSINE),
    )

    # 2. Docs folder se files parhna
    # Docs folder ko current directory se dhoond rahe hain
    docs_path = os.path.join("docs", "*.md")
    files = glob.glob(docs_path)
    
    if not files:
        print("❌ Error: 'docs' folder mein koi .md files nahi milin!")
        return

    points = []
    for idx, file_path in enumerate(files):
        try:
            # Try UTF-8 first, then fallback to other encodings
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='utf-16') as f:
                    content = f.read()
            
            # Dummy vector (4 numbers)
            dummy_vector = [0.1, 0.2, 0.3, 0.4] 
            
            points.append(PointStruct(
                id=idx,
                vector=dummy_vector,
                payload={
                    "filename": os.path.basename(file_path), 
                    "text": content[:1000] # Pehle 1000 characters
                }
            ))
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")

    # 3. Qdrant mein upload karna
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Success! {len(files)} files Qdrant Cloud par upload ho gayi hain.")

if __name__ == "__main__":
    start_ingestion()