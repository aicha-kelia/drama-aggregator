

import cloudinary
import cloudinary.uploader
import os
import time

# PASTE YOUR CREDENTIALS HERE
cloudinary.config(
    cloud_name="dobqw9fa9",
    api_key="971324672167161",
    api_secret="_Yuhs0gVWh8pAWAOVSI0MQJsaYc"
)

LOCAL_FOLDER = r"C:\Users\PC\OneDrive\Desktop\Hybrid_Projects\dramahere\media\thumbnails"
CLOUDINARY_FOLDER = "dramahere_thumbnails"

uploaded_urls = {}

for filename in os.listdir(LOCAL_FOLDER):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        filepath = os.path.join(LOCAL_FOLDER, filename)
        
        # RETRY LOGIC - try 3 times before giving up
        for attempt in range(3):
            try:
                result = cloudinary.uploader.upload(
                    filepath,
                    folder=CLOUDINARY_FOLDER,
                    public_id=os.path.splitext(filename)[0],
                    overwrite=False
                )
                
                url = result['secure_url']
                uploaded_urls[filename] = url
                print(f"✅ {filename} → {url}")
                break  # Success - exit retry loop
                
            except Exception as e:
                if attempt < 2:  # If not last attempt
                    print(f"⚠️ {filename} failed (attempt {attempt+1}/3), retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"❌ {filename} FAILED after 3 attempts: {e}")

# Save URLs to file
with open('cloudinary_urls.txt', 'w') as f:
    for filename, url in uploaded_urls.items():
        f.write(f"{filename}|{url}\n")

print(f"\n🎉 DONE! {len(uploaded_urls)} images processed")
print("URLs saved to cloudinary_urls.txt")