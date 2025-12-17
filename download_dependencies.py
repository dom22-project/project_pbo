import urllib.request
import os

# Create directories
os.makedirs('static/vendor/select2/css', exist_ok=True)
os.makedirs('static/vendor/select2/js', exist_ok=True)

# Files to download
files = [
    {
        'url': 'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
        'path': 'static/vendor/select2/css/select2.min.css'
    },
    {
        'url': 'https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css',
        'path': 'static/vendor/select2/css/select2-bootstrap-5-theme.min.css'
    },
    {
        'url': 'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
        'path': 'static/vendor/select2/js/select2.min.js'
    }
]

print("Downloading Select2 dependencies...")
for file in files:
    print(f"Downloading {file['url']}...")
    try:
        urllib.request.urlretrieve(file['url'], file['path'])
        print(f"✓ Saved to {file['path']}")
    except Exception as e:
        print(f"✗ Error downloading {file['url']}: {e}")

print("\nDownload complete!")
print("All dependencies are now available locally in static/vendor/select2/")
