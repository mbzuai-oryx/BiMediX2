import os
import requests
import zipfile
from io import BytesIO

os.makedirs("images", exist_ok=True)

slake_out = "tmp/slake"
os.makedirs(slake_out, exist_ok=True)

# Download and extract
print("Downloading dataset...")
response = requests.get("https://huggingface.co/datasets/BoKelvin/SLAKE/resolve/main/imgs.zip")
response.raise_for_status()

print("Extracting files...")
with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
    zip_ref.extractall(slake_out)

print("Organizing images...")
for _,dirs,files in os.walk(os.path.join(slake_out,"imgs")):
    for dir in dirs:
        for _,_,files in os.walk(os.path.join(slake_out,"imgs",dir)):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):
                    src = os.path.join(slake_out,"imgs",dir,file)
                    dest = f"{os.path.join("images",dir)}_{file}"
                    os.system(f"mv {src} {dest}")

print("Downloading SLAKE dataset images...")

rad_out = "tmp/rad"
os.makedirs(rad_out, exist_ok=True)

os.system("kaggle datasets download -d shashankshekhar1205/vqa-rad-visual-question-answering-radiology --unzip -p tmp/rad")

print("Organizing images...")
os.system("mv tmp/rad/VQA_RAD\ Image\ Folder/* images/")

print("Downloading Path-VQA dataset images...")
path_ds = load_dataset("flaviagiammarino/path-vqa", split="train")

imgs = []
i = 0
for sample in path_ds:
    img = sample['image']
    if img not in imgs:
        imgs.append(img)
        i+=1
        img_name = f"path-vqa_{i}.jpg"
        img.save(os.path.join("images", img_name))

print("Cleaning up temporary files...")
os.system("rm -rf tmp/")
