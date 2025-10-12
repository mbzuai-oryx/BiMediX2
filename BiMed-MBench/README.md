# BiMed-MBench Evaluation

A bilingual benchmark for evaluating Vision-Language Models (VLMs) on biomedical imaging tasks in English and Modern Standard Arabic.

## Installation

### Install LLaVA-pp

Install [LLaVA-pp](https://github.com/mbzuai-oryx/LLaVA-pp?tab=readme-ov-file#installation) by following the installation guide.

### Set OpenAI API Key

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Quick Start

### Evaluate on English

```bash
./eval.sh
```

Evaluates `MBZUAI/BiMediX2-8B` model on English test set.

### Evaluate on Arabic

```bash
./eval_ara.sh
```

Evaluates `MBZUAI/BiMediX2-8B-BI` bilingual model on Arabic test set.

## Usage

The evaluation pipeline has three steps:

### Step 1: Generate Model Answers

```bash
python gen_ans.py <model_path> <language>
```

- `language`: `eng` or `ara`
- Output: `./data/eval_out_files/{model_name}/{language}_ans.jsonl`

### Step 2: Evaluate with GPT-4o

**English:**
```bash
python eval/eval_multimodal_chat_gpt_score.py \
    --answers-file data/eval_out_files/{model_name}/eng_ans.jsonl \
    --question-file data/test_sets/bimed-mbench_eng.jsonl \
    --scores-file data/eval_out_files/{model_name}/eng_score.jsonl
```

**Arabic:**
```bash
python eval/eval_multimodal_chat_gpt_score_ara.py \
    --answers-file data/eval_out_files/{model_name}/ara_ans.jsonl \
    --question-file data/test_sets/bimed-mbench_ara.jsonl \
    --scores-file data/eval_out_files/{model_name}/ara_score.jsonl
```

### Step 3: Summarize Results

```bash
python eval/summarize_gpt_review.py \
    --scores-file data/eval_out_files/{model_name}/{language}_score.jsonl
```

Output: `./data/eval_out_files/{model_name}/{language}_results.txt`

## Custom Model Inference

For custom models, implement your own inference in `gen_ans.py` by replacing the `bimedix_inference.Inference` class with your model's inference code.
