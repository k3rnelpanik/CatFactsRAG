dataset =[]
with open('facts.txt', 'r', encoding = 'utf-8') as file:
    dataset = file.readlines()
    print(f'Loaded {len(dataset)} lines')
import ollama
EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

def add_chunk(chunk):
    embedding = ollama.embed(EMBEDDING_MODEL, chunk)['embeddings'][0]
    VECTOR_DB.append((chunk, embedding))

for i, chunk in enumerate(dataset):
    add_chunk(chunk)
    print(f'Added chunk {i+1}/{len(dataset)}')

# Simple Retrieval function
def cosine_similarity(a,b):
    dot = sum(x*y for x,y in zip(a,b))
    norm_a = sum(x*x for x in a) ** 0.5
    norm_b = sum(x*x for x in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

#Retrieval function
def retrieve(query, top_n=3):
    query_embedding = ollama.embed(EMBEDDING_MODEL, query)['embeddings'][0]

    similarities = [(chunk, cosine_similarity(query_embedding, embedding)) for chunk, embedding in VECTOR_DB]
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:top_n]

# Loopback
st=1
while(st==1):
    # Example query
    input_query = input("Ask a question about cats...\n")
    retrieved = retrieve(input_query)

    print('Retrieved Facts:\n')
    print('----------------\n')
    for chunk, similarity in retrieved:
        print(f'[{similarity:.2f}] {chunk}')
    instruction_prompt = "\n\nBased on the above facts and above facts alone, answer the following question:\n"
    instruction_prompt += '\n'.join([chunk for chunk, similarity in retrieved])

    stream = ollama.chat(
        model = LANGUAGE_MODEL,
        messages = [
            {'role':'user', 'content': input_query},
            {'role':'assistant', 'content': instruction_prompt}
        ],
        stream = True,
    )

    # Print response in real-time
    print('Response:')
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    print('----------------\n')
    st=int(input('\nPress 1 to ask another question or 0 to exit...\n'))