import os
import glob
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
COLLECTION_NAME = "physical_ai_docs"

def start_ingestion():
    print("🚀 Simple Upload shuru ho raha hai...")
    
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
    
    # Vector size 4 rakha hai sirf formality ke liye
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=4, distance=Distance.COSINE),
    )

    docs_path = os.path.join("docs", "*.md")
    files = glob.glob(docs_path)
    
    points = []
    for idx, file_path in enumerate(files):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if content.strip():
                points.append(PointStruct(
                    id=idx,
                    vector=[0.1, 0.2, 0.3, 0.4], # Dummy vector
                    payload={"filename": os.path.basename(file_path), "text": content[:5000]}
                ))
                print(f"✅ Saved to list: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"🎉 Success! {len(points)} files Qdrant par chali gayi hain.")

if __name__ == "__main__":
    start_ingestion()