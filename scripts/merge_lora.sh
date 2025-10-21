# #!/bin/bash

python scripts/merge_lora_weights.py \
    --model-path ./checkpoints/BiMediX2_llava_8B_finetune_lora \
    --model-base meta-llama/Meta-Llama-3.1-8B-Instruct \
    --save-model-path ./checkpoints/BiMediX2_8B
