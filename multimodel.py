import os
import numpy as np
import faiss
import fitz 
from PIL import Image
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

clip_model = SentenceTransformer("clip-ViT-B-32")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def extract_data(pdf_path):
    doc = fitz.open(pdf_path)

    texts = []
    image_paths = []

    os.makedirs("images", exist_ok=True)

    for page_num in range(len(doc)):
        page = doc[page_num]

        texts.append(page.get_text())

        for img_index, img in enumerate(page.get_images(full=True)):
            base_image = doc.extract_image(img[0])

            img_path = f"images/page{page_num}_{img_index}.png"

            with open(img_path, "wb") as f:
                f.write(base_image["image"])

            image_paths.append(img_path)

    return texts, image_paths

def build_index(texts, image_paths):
    documents = []

    for t in texts:
        documents.append({"type": "text", "content": t})

    for path in image_paths:
        documents.append({"type": "image", "path": path})

    text_embeddings = clip_model.encode(texts)
    images = [Image.open(p) for p in image_paths]
    image_embeddings = clip_model.encode(images)

    all_embeddings = np.vstack([text_embeddings, image_embeddings]).astype("float32")

    faiss.normalize_L2(all_embeddings)

    index = faiss.IndexFlatIP(all_embeddings.shape[1])
    index.add(all_embeddings)

    return index, documents

def query_rag(query, index, documents, k=5):
    query_vec = clip_model.encode([query]).astype("float32")
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, k)

    results = [documents[i] for i in indices[0]]
    return results

def generate_answer(query, results):
    parts = [f"Query: {query}"]

    for res in results:
        if res["type"] == "text":
            parts.append(f"Text:\n{res['content']}")
        else:
            parts.append(f"Image: Image.open({res['path']})")

    full_message = "\n\n".join(parts)

    messages = [{"role": "user", "content": full_message}]

    response = llm.invoke(messages)
    return response.content

if __name__ == "__main__":
    pdf_path = r"C:\Users\jetty\OneDrive\Desktop\Resume_Builder\minion-tech.pdf"

    texts, image_paths = extract_data(pdf_path)

    index, documents = build_index(texts, image_paths)

    user_query = "What are the technical skills of this person?"
    
    results = query_rag(user_query, index, documents)

    answer = generate_answer(user_query, results)

    print("\n===== FINAL ANSWER =====\n")
    print(answer)

