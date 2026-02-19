import json
import os
from utils import download_image

def main():
    files = [
        'thesouledstore.jsonl',
        'final_tss.jsonl',
        'teepublic_quick.jsonl',
        'threadless_scraped.jsonl',
        'final_asos.jsonl'
    ]
    
    urls = set()
    for f_path in files:
        if not os.path.exists(f_path): continue
        with open(f_path, 'r') as f:
            for line in f:
                try:
                    item = json.loads(line)
                    # Check different image structures
                    if 'images' in item:
                        if isinstance(item['images'], list):
                            for img in item['images']:
                                if isinstance(img, dict): urls.add(img.get('url'))
                                else: urls.add(img)
                        elif isinstance(item['images'], dict):
                            if 'all' in item['images']:
                                for img in item['images']['all']: urls.add(img)
                            if 'primary' in item['images']:
                                urls.add(item['images']['primary'])
                    if 'image_urls' in item:
                        for u in item['image_urls']: urls.add(u)
                except: continue
                
    print(f"Found {len(urls)} unique image URLs. Starting download...")
    count = 0
    for url in urls:
        if not url: continue
        path = download_image(url)
        if path:
            count += 1
            if count % 50 == 0:
                print(f"Downloaded {count} images...")
                
    print(f"Finished! Total images now: {count}")

if __name__ == "__main__":
    main()
