model_path="MBZUAI/BiMediX2-8B"
model_name="${model_path##*/}"
language="eng"

echo $model_path
echo $model_name
echo $language

# Generate Responses
python3 gen_ans.py ${model_path} ${language} && \

# Evaluate
python3 eval/eval_multimodal_chat_gpt_score.py \
    --answers-file data/eval_out_files/${model_name}/${language}_ans.jsonl \
    --question-file data/test_sets/bimed-mbench_eng.jsonl \
    --scores-file data/eval_out_files/${model_name}/${language}_score.jsonl && \

# Summarize
python3 eval/summarize_gpt_review.py \
    --scores-file data/eval_out_files/${model_name}/${language}_score.jsonl