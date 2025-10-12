import torch
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria
from llava.model.builder import load_pretrained_model
from transformers import TextIteratorStreamer
from threading import Thread
from PIL import Image
from typing import List
from llava.conversation import Conversation, SeparatorStyle

conv_llama3 = Conversation(
    system="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nA chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.""",
    roles=("<|start_header_id|>user<|end_header_id|>\n\n", "<|start_header_id|>assistant<|end_header_id|>\n\n"),
    version="llama3",
    messages=(),
    offset=0,
    sep_style=SeparatorStyle.MPT,
    sep="<|eot_id|>",
)

class Inference:
    def __init__(self, model_path="BiMediX2-8B"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.image_processor = None
        self.is_multimodal = True
        print("==============================================")
        print(f"generating with model: {self.model_path}")
        print("==============================================")

        self.setup()

    def setup(self):
        self.model_name = get_model_name_from_path(self.model_path)+"_llava" # for llava repo internal checks
        self.tokenizer, self.model, self.image_processor, self.context_len = load_pretrained_model(self.model_path, model_name=self.model_name, model_base=None, load_8bit=False, load_4bit=False, device='cuda', use_flash_attn=True)

    @torch.inference_mode()
    def generate_stream(self, prompt, images=None, kwargs={}):
        ori_prompt = prompt
        num_image_tokens = 0
        if images is not None and len(images) > 0 and self.is_multimodal:
            if len(images) > 0:
                if len(images) != prompt.count(DEFAULT_IMAGE_TOKEN):
                    raise ValueError("Number of images does not match number of <image> tokens in prompt")

                image_sizes = [image.size for image in images]
                images = process_images(images, self.image_processor, self.model.config)

                if type(images) is list:
                    images = [image.to(self.model.device, dtype=torch.float16) for image in images]
                else:
                    images = images.to(self.model.device, dtype=torch.float16)

                replace_token = DEFAULT_IMAGE_TOKEN
                if getattr(self.model.config, 'mm_use_im_start_end', False):
                    replace_token = DEFAULT_IM_START_TOKEN + replace_token + DEFAULT_IM_END_TOKEN
                prompt = prompt.replace(DEFAULT_IMAGE_TOKEN, replace_token)

                num_image_tokens = prompt.count(replace_token) * self.model.get_vision_tower().num_patches
            else:
                images = None
                image_sizes = None
            image_args = {"images": images, "image_sizes": image_sizes}
        else:
            images = None
            image_args = {}

        temperature = float(kwargs.get("temperature", float(0.1)))
        top_p = float(kwargs.get("top_p", 1.0))
        max_context_length = getattr(self.model.config, 'max_position_embeddings', 2048)
        max_new_tokens = int(kwargs.get("max_new_tokens", 1024))
        stop_str = kwargs.get("stop", conv_llama3.sep if conv_llama3.sep_style in [SeparatorStyle.SINGLE, SeparatorStyle.MPT] else conv_llama3.sep2)
        do_sample = True if temperature > 0.001 else False

        input_ids = tokenizer_image_token(prompt, self.tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(self.model.device)
        keywords = [stop_str]
        stopping_criteria = KeywordsStoppingCriteria(keywords, self.tokenizer, input_ids)
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True, timeout=15)

        max_new_tokens = min(max_new_tokens, max_context_length - input_ids.shape[-1] - num_image_tokens)

        if max_new_tokens < 1:
            return ori_prompt + "Exceeds max token length. Please start a new conversation, thanks."

        thread = Thread(target=self.model.generate, kwargs=dict(
            inputs=input_ids,
            do_sample=do_sample,
            temperature=temperature,
            top_p=top_p,
            max_new_tokens=max_new_tokens,
            streamer=streamer,
            stopping_criteria=[stopping_criteria],
            use_cache=True,
            **image_args
        ))
        thread.start()

        generated_text = ""
        for new_text in streamer:
            generated_text += new_text
            if generated_text.endswith(stop_str):
                generated_text = generated_text[:-len(stop_str)]
        return generated_text

    def gen_answer(self, question, image):# image = [Image.open(image).convert('RGB')]
        conv = conv_llama3.copy()
        if image==None:
            question = question.replace('<image>','').strip()
            images = None
        if image!=None:
            if '<image>' not in question:
                question = f"<image>\n{question.strip()}"
            images = [Image.open(image).convert('RGB')]
        conv.append_message(conv.roles[0], question)
        conv.append_message(conv.roles[1], None)

        prompt = conv.get_prompt()
        out = self.generate_stream(prompt,images)

        print("----------------------------------")
        print(prompt)
        print(out)
        print("----------------------------------")
        return out