# BiMediX2 Training

## Prerequisites

### 1. Install LLaVA-pp

Install [LLaVA-pp](https://github.com/mbzuai-oryx/LLaVA-pp?tab=readme-ov-file#installation) for LLaMA-3-V by following the installation guide.

## Data Preparation

### 2. Download Data JSON Files

Download the required data files for training from huggingface:

- **Stage 1 Data**: [`BiMed-V_stage1.json`](https://huggingface.co/datasets/MBZUAI/BiMed-V-1.6M/blob/main/BiMed-V_stage1.json)
- **Stage 2 Data**: [`BiMed-V_stage2.json`](https://huggingface.co/datasets/MBZUAI/BiMed-V-1.6M/blob/main/BiMed-V_stage2.json)

### 3. Download Images

Use the provided script to download the required PMC, Slake-VQA, Rad-VQA, and Path-VQA images for training:

```bash
python scripts/download_pmc_images.py

# Setup Kaggle before this...

python scripts/download_slake_rad_path_images.py
```

**Important Notes:**
- The PMC script downloads images from PMC tar URLs
- It requires the `llava_med_image_urls.jsonl` file (available from [LLaVA-Med repository](https://github.com/microsoft/LLaVA-Med/blob/main/data/llava_med_image_urls.jsonl))
- Slake, Rad and Path VQA is available from their respective model cards. ([Slake](https://huggingface.co/datasets/BoKelvin/SLAKE), [Rad-VQA](https://www.kaggle.com/datasets/shashankshekhar1205/vqa-rad-visual-question-answering-radiology/data), [Path-VQA](https://huggingface.co/datasets/flaviagiammarino/path-vqa))
- Images will be downloaded to `./images/` directory
- The script supports resumable downloads and handles deduplication
- Adjust the `max_workers` parameter in the script based on your system capabilities
- The script currently downloads images for stage 2 data by default. Modify line 24 to use stage 1 data if needed:
  ```python
  # For stage 1:
  dataset_json = load_jsonl("BiMed-V_stage1.json")
  # For stage 2:
  dataset_json = load_jsonl("BiMed-V_stage2.json")
  ```

## Training

### 4. Stage 1 Training (Pretraining)

Run the stage 1 training script to pretrain the multimodal projector:

```bash
./scripts/stage1_train.sh
```

**Stage 1 Configuration:**
- **Purpose**: Pretrains the multimodal projector (MM-MLP) 
- **Data**: Uses `BiMed-V_stage1.json`
- **Base Model**: `meta-llama/Meta-Llama-3.1-8B-Instruct`
- **Vision Tower**: `openai/clip-vit-large-patch14-336`
- **Training**: Only tunes the MM-MLP adapter (`tune_mm_mlp_adapter True`)
- **Output**: Saves checkpoints to `./checkpoints/BiMediX2_llava_8B_pretrain`

**Before running, make sure to:**
- Update `<image_folder_path>` in the script to point to your images directory
- Ensure you have sufficient GPU memory

### 5. Stage 2 Training (Fine-tuning)

Run the stage 2 training script to fine-tune the model:

```bash
./scripts/stage2_train.sh
```

**Stage 2 Configuration:**
- **Purpose**: Fine-tunes the model with LoRA (Low-Rank Adaptation)
- **Data**: Uses `BiMed-V_stage2.json`
- **LoRA Settings**: Rank 8, Alpha 16
- **Pretrained Projector**: Loads from stage 1 output (`./checkpoints/BiMediX2_llava_8B_pretrain/mm_projector.bin`)
- **Output**: Saves LoRA weights to `./checkpoints/BiMediX2_llava_8B_finetune_lora`

**Before running, make sure to:**
- Complete stage 1 training successfully
- Update `<image_folder_path>` in the script to point to your images directory
- Ensure the pretrained MM projector path is correct

## Output

After successful training:
- **Stage 1**: MM projector weights in `./checkpoints/BiMediX2_llava_8B_pretrain/`
- **Stage 2**: LoRA adapter weights in `./checkpoints/BiMediX2_llava_8B_finetune_lora/`

Use the `merge_lora.sh` script to merge LoRA weights with the base model.