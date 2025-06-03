import pandas as pd

# LlamaIndex / GPT Index imports
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import Document

# 1) Read Excel into a pandas DataFrame
print("Reading")
df = pd.read_excel("./data_cleaning/courses.xlsx")

# 2) Create a Document object for each row, including text + metadata
documents = []
print("making docs")
for idx, row in df.iterrows():
    # For text, you can combine fields like course_code, name, description, etc.
    # Or just use the description if that's the main body of text for semantic search.
    text_content = (
        f"Code: {row['code']}. Title: {row['name']}. "
        f"Prerequisites: {row['prerequisites']}. Corequisites: {row['corequisites']} "
        f"Description: {row['description']}"
    )

    # Convert row values into metadata dict
    metadata_dict = {
        "course_code": row["code"],
        "course_name": row["name"],
        "prerequisites": row["prerequisites"]
        # Add more fields if needed, e.g. "credits": row["credits"]
    }

    doc = Document(text=text_content, metadata=metadata_dict)
    documents.append(doc)

# 3) Pick a local embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4) Build a vector store index with your documents
print("making index")
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

# Optional: persist the index to disk
print("persisting")
index.storage_context.persist(persist_dir="./course_index_jsonTags")


