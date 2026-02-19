import requests
import os
import hashlib

def download_image(url, folder='images'):
    if not url:
        return None
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Create a unique filename based on the URL
        ext = url.split('.')[-1].split('?')[0]
        if len(ext) > 4 or len(ext) < 3: ext = 'jpg'
        filename = hashlib.md5(url.encode()).hexdigest() + '.' + ext
        filepath = os.path.join(folder, filename)
        
        if os.path.exists(filepath):
            return filepath
            
        r = requests.get(url, stream=True, timeout=10)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            return filepath
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None
