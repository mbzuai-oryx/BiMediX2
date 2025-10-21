from tqdm import tqdm
import os
import json
import requests
import tarfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return data

PROGRESS_FILE = "./download_progress.json"

# dataset_json = load_jsonl("BiMed-V_stage1.json") # Uncomment for stage 1
dataset_json = load_jsonl("BiMed-V_stage2.json")
image_urls = load_jsonl("llava_med_image_urls.jsonl") # https://github.com/microsoft/LLaVA-Med/blob/main/data/llava_med_image_urls.jsonl

def load_progress():
    """Load progress from file if it exists."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return set(json.load(f))
        except (json.JSONDecodeError, TypeError):
            return set()
    return set()

def save_progress(completed_images):
    """Save progress to file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(list(completed_images), f)

def update_progress(image_name, completed_images, lock):
    """Thread-safe progress update."""
    with lock:
        completed_images.add(image_name)
        # Save progress every 10 completed items to reduce I/O
        if len(completed_images) % 10 == 0:
            save_progress(completed_images)

def process_sample(sample, image_urls_map, completed_images, progress_lock):
    """Process a single sample by downloading and extracting the image."""
    image_path = f"./images/{sample['image']}"
    
    # Check if already completed (from progress file or file exists)
    if sample['image'] in completed_images or os.path.exists(image_path):
        return False
    
    try:
        info = image_urls_map['_'.join(sample['id'].split('_')[:-1])]
        pmc_tar_url = info['pmc_tar_url']
        pmc_tar_name = os.path.basename(pmc_tar_url)
        
        # Use a lock to prevent filename conflicts
        lock = threading.Lock()
        with lock:
            tmp_dir = f"./tmp/{threading.get_ident()}"
            os.makedirs(tmp_dir, exist_ok=True)
            tmp_tar_path = f"{tmp_dir}/{pmc_tar_name}"

        # Download tar file to tmp directory
        with requests.get(pmc_tar_url, stream=True) as r:
            r.raise_for_status()
            with open(tmp_tar_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Extract tar file
        with tarfile.open(tmp_tar_path, "r:gz") as tar:
            tar.extractall(path=tmp_dir)

        # Copy the image
        src_image_path = os.path.join(tmp_dir, info['image_file_path'])
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        shutil.move(src_image_path, image_path)

        # Cleanup
        os.remove(tmp_tar_path)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        
        # Update progress
        update_progress(sample['image'], completed_images, progress_lock)
        return True
    except Exception as e:
        print(f"Error processing sample {sample['id']}: {e}")
        # Cleanup on error
        if os.path.exists(tmp_tar_path):
            os.remove(tmp_tar_path)
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
        return False

# Deduplicate samples by image filename, keeping the first occurrence
seen_images = set()
unique_dataset_json = []
for sample in dataset_json:
    if sample['image'] not in seen_images:
        seen_images.add(sample['image'])
        unique_dataset_json.append(sample)

print(f"Deduplicated: {len(dataset_json)} -> {len(unique_dataset_json)} unique images")

dataset_json = unique_dataset_json
image_urls_map = {item['pair_id']: item for item in image_urls}

# Load progress from previous runs
completed_images = load_progress()

# Add already downloaded images to completed_images
for sample in dataset_json:
    if os.path.exists(f"./images/{sample['image']}"):
        completed_images.add(sample['image'])

progress_lock = threading.Lock()

os.makedirs("./tmp", exist_ok=True)
os.makedirs("./images", exist_ok=True)

# Clean up any incomplete tmp directories from previous runs
if os.path.exists("./tmp"):
    for item in os.listdir("./tmp"):
        item_path = os.path.join("./tmp", item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path, ignore_errors=True)

# Process samples in parallel
max_workers = 48  # Adjust based on your system's capabilities
samples_to_process = [s for s in dataset_json if s['image'] not in completed_images and not os.path.exists(f"./images/{s['image']}")]
print(f"Processing {len(samples_to_process)} out of {len(dataset_json)} samples...")
print(f"Already completed: {len(completed_images)} images")

# for sample in tqdm(samples_to_process):
#     process_sample(sample, image_urls_map)

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Submit all tasks
    future_to_sample = {
        executor.submit(process_sample, sample, image_urls_map, completed_images, progress_lock): sample['image'] 
        for sample in samples_to_process
    }
    
    # Process as they complete
    for future in tqdm(as_completed(future_to_sample), total=len(future_to_sample)):
        image_name = future_to_sample[future]
        try:
            success = future.result()
            if not success:
                pass  # Already handled in process_sample
        except Exception as exc:
            print(f"Image {image_name} generated an exception: {exc}")

# Final progress save
save_progress(completed_images)
print(f"Download complete. Total completed: {len(completed_images)} images")

