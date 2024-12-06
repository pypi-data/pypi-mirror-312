import DatasetGeneration_functions

# Load the document
txt_path = r"C:\Users\lucas\Desktop\BDD_Helico\Owners Manuel Fama Kiss.txt"
document = DatasetGeneration_functions.load_txt_file(txt_path)

from chonkie import SemanticChunker

from chonkie import SemanticChunker
from chonkie.embeddings import BaseEmbeddings

model_name = r"C:\Users\lucas\aait_store\Models\NLP\all-mpnet-base-v2"
model = model_name
chunker = SemanticChunker(
    embedding_model=model,  # Default model
    similarity_threshold=0.3,  # Similarity threshold (0-1)
    chunk_size=1024,  # Maximum tokens per chunk
    initial_sentences=5  # Initial sentences per chunk
)

chunks = chunker.chunk(document)
chunks1=[]
for chunk in chunks:
    chunks1.append(chunk.text)

for c in chunks1:
    print("\n\nCHUNK------:", c)

