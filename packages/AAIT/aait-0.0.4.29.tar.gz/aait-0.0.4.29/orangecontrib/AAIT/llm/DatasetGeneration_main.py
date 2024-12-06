import time
import json
import ntpath
import DatasetGeneration_functions
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer


txt_path = r"C:\Users\lucas\Desktop\BDD_Helico\manuel_volFamaKiss.txt"
filename = ntpath.basename(txt_path).replace(".txt", "")

# Load the document
document = DatasetGeneration_functions.load_txt_file(txt_path)

# Generate a summary of the document for context
path = r"C:\Users\lucas\aait_store\Models\NLP\Llama-3-8B-Instruct-Gradient-1048k-Q6_K.gguf"
llama1048 = Llama(path, n_ctx=31000, n_gpu_layers=-1)
theme = DatasetGeneration_functions.generate_summary(model=llama1048, text=document, max_tokens=100)
print("Thème du document :", theme + ".")
llama1048.close()

# Chunk the document
chunks = DatasetGeneration_functions.chunk_string_with_overlap(document, chunk_size=600, overlap=0.5)

# Load models: Solar to generate questions/answers and MPNET to verify if they are repeated
path = r"C:\Users\lucas\aait_store\Models\NLP\solar-10.7b-instruct-v1.0.Q6_K.gguf"
solar = Llama(path, n_ctx=4096, n_gpu_layers=-1, verbose=False)
path = r"C:\Users\lucas\aait_store\Models\NLP\all-mpnet-base-v2"
mpnet = SentenceTransformer(path)

# Loop over all chunks
all_questions = []
all_answers = []
for i in range(1, 5):#len(chunks)):
    t = time.time()
    print(f"----------------\nGeneration {i}/{len(chunks)}\n----------------")
    chunk = chunks[i]
    questions, answers = DatasetGeneration_functions.generate_dataset_on_chunk(model=solar, embedder=mpnet, chunk=chunk,
                                                                               threshold=0.95, max_repeat=20, safety_limit=100)
    all_questions += questions
    all_answers += answers

    # Creating a list of dictionaries
    result = [{"instruction": question, "response": answer} for question, answer in zip(questions, answers)]
    data = {"theme": theme, "data": result}
    result_chunk = [{"chunk": chunk}]

    # Save the list to a JSON file
    filepath = rf"C:\Users\lucas\Desktop\HelicoFinetuning_json\{filename}_questions_chunk_{i}.json"
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    # Save the list to a JSON file
    filepath = rf"C:\Users\lucas\Desktop\HelicoFinetuning_json\{filename}_chunk_{i}.json"
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(result_chunk, file, ensure_ascii=False, indent=4)
    print(f"\n------------------\nTime for generation on chunk {i}: {time.time() - t:.2f}s\n")

print(f"Number of chunks: {len(chunks)}")
print(f"Number of questions: {len(all_questions)}")
