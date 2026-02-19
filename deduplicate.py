import json
import os
import requests
from PIL import Image
import imagehash
from io import BytesIO

def get_image_hash(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        return str(imagehash.phash(img))
    except Exception as e:
        print(f"Error hashing {url}: {e}")
        return None

def deduplicate(input_files, output_file):
    hashes = {}
    unique_items = []
    
    for file in input_files:
        if not os.path.exists(file):
            continue
        with open(file, 'r') as f:
            for line in f:
                item = json.loads(line)
                primary_img = item.get('images', {}).get('primary')
                if not primary_img:
                    unique_items.append(item)
                    continue
                
                # Using image hash for deduplication
                # For efficiency in this script, we'll use the URL as a first pass,
                # then maybe the actual image hash if requested.
                # Given the instruction, let's try actual hashing for a few.
                img_hash = get_image_hash(primary_img)
                if img_hash not in hashes:
                    hashes[img_hash] = True
                    unique_items.append(item)
                else:
                    print(f"Duplicate found: {item['url']}")

    with open(output_file, 'w') as f:
        for item in unique_items:
            f.write(json.dumps(item) + '\n')
    print(f"Deduplication complete. {len(unique_items)} unique items saved.")

if __name__ == "__main__":
    import sys
    files = sys.argv[1:-1]
    out = sys.argv[-1]
    deduplicate(files, out)
