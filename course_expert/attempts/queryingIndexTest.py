from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load your index (already created and persisted)
storage_context = StorageContext.from_defaults(persist_dir="./course_index_jsonTags")
index = load_index_from_storage(storage_context)

# Build metadata filters
filter_conditions = [ExactMatchFilter(key="course_code", value="MATH 442")]
metadata_filters = MetadataFilters(filters=filter_conditions)

# Create query openAI_engine with filters
query_engine = index.as_query_engine(
    similarity_top_k=3,
    filters=metadata_filters
)

# Ask your question
question = "What are the prerequisites for MATH 442?"
response = query_engine.query(question)
print(response.response)