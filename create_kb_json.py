import json
import os

# Paths
knowledge_base_dir = "data/knowledge_base"
output_file = "data/processed/knowledge_base.json"

documents = []

print("Reading knowledge base files...")

for filename in os.listdir(knowledge_base_dir):
    if filename.endswith('.txt'):
        filepath = os.path.join(knowledge_base_dir, filename)
        print(f"  Processing: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into chunks of ~500 chars
        chunk_size = 500
        overlap = 50
        start = 0
        chunk_id = 0
        
        while start < len(content):
            chunk = content[start:start + chunk_size].strip()
            if chunk:
                doc_id = filename.replace(".txt", "") + "_" + str(chunk_id)
                documents.append({
                    "id": doc_id,
                    "source": filename,
                    "content": chunk,
                    "type": "knowledge_base"
                })
                chunk_id += 1
            start += chunk_size - overlap

print(f"\nTotal chunks created: {len(documents)}")

# Save to JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(documents, f, indent=2)

print(f"Saved to: {output_file}")
