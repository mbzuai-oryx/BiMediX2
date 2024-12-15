# BiMediX2 : Bio-Medical EXpert LMM for Diverse Medical Modalities

<p align="center">
    <img src="https://i.imgur.com/waxVImv.png" alt="BiMediX2">
</p>

#### [Sahal Shaji Mullappilly](https://scholar.google.com/citations?user=LJWxVpUAAAAJ&hl=en)\*, [Mohammed Irfan K](https://scholar.google.com/citations?user=GJp0keYAAAAJ&hl=en)*, [Sara Pieri](https://scholar.google.com/citations?user=jLNKLsgAAAAJ&hl=en&oi=ao), [Saeed Yahya Alseiari](https://ssmc.ae/doctors/dr-saeed-alseiari/), [Shanavas Cholakkal](https://www.researchgate.net/profile/Shanavas-Cholakkal), [Khaled Aldahmani](https://www.seha.ae/doctor-detail/327), [Fahad Khan](https://sites.google.com/view/fahadkhans/home), [Rao Muhammad Anwer](https://scholar.google.com/citations?hl=en&authuser=1&user=_KlvMVoAAAAJ), [Salman Khan](https://salman-h-khan.github.io/), [Timothy  Baldwin](https://scholar.google.com/citations?user=wjBD1dkAAAAJ&hl=en), and [Hisham Cholakkal](https://scholar.google.com/citations?hl=en&user=bZ3YBRcAAAAJ)

\**Equally contributing first authors*

#### **Mohamed Bin Zayed University of Artificial Intelligence (MBZUAI), UAE**
[![Website](https://img.shields.io/badge/Project-Website-87CEEB)](https://github.com/mbzuai-oryx/BiMediX2)
[![Paper](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)](https://arxiv.org/abs/2412.07769)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Model-F9D371)](https://huggingface.co/collections/MBZUAI/bimedix2-675ee7528464dfd03f746127)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)](https://github.com/mbzuai-oryx/BiMediX/blob/main/LICENSE.txt)

## 📢 Latest Updates

- **Dec-15-24**: Our Model checkpoints are released on **_HuggingFace_** [link](https://huggingface.co/collections/MBZUAI/bimedix2-675ee7528464dfd03f746127). 🔥
- **Dec-11-24**: BiMediX2 Technical Report is released [link](https://arxiv.org/abs/2412.07769). 🔥
- **Dec-02-24**: BiMediX2 is featured by **_AI at Meta_** [link](https://ai.meta.com/blog/bimedix-built-with-llama/). 🔥
- **Sep-24-24**: BiMediX2 wins the **_Meta Llama Impact Innovation Award_** [link](https://ai.meta.com/blog/llama-impact-grant-innovation-award-winners-2024/). 🔥

## 	👩‍⚕️ Overview


Introducing **BiMediX2**, the first bilingual (Arabic-English) Bio-Medical Expert Large Multimodal Model (LMM) designed for advanced medical image understanding and applications. Built on the Llama 3.1 architecture, BiMediX2 seamlessly integrates text and visual modalities to enable multilingual interactions, including text-based queries and multi-turn conversations involving medical images. Trained on a diverse bilingual and multimodal healthcare dataset of 1.6M samples, it achieves state-of-the-art performance across various benchmarks. BiMediX2 outperforms recent models in multimodal medical evaluations, delivering over 9% improvement in English and 20% in Arabic evaluations, and excelling in tasks like medical VQA, Report Generation, and Summarization.

---

## 🏆 Contributions

Our key contributions are as follows:

- We introduce the _**first bilingual medical LMM**_ that achieves state-of-the-art results on VLM evaluation benchmarks across various medical image modalities, while also excelling on medical LLM evaluation benchmarks.
- We curated a comprehensive _**Arabic-English multimodal bilingual instruction set**_ named _**BiMed-V**_ comprising over _**1.6M**_ instructions.
- We introduce the first bilingual GPT-4o-based _**medical LMM benchmark**_ named _**BiMed-MBench**_, consisting of 286 medical queries in English and Arabic across various medical image modalities, fully verified by medical experts.
- Our BiMediX2 LLM outperforms GPT-4 by _**more than 8%**_ on the USMLE benchmark and by _**more than 9%**_ in UPHILL factual accuracy evaluations.
- Our BiMediX2 LMM achieves state-of-the-art results on BiMed-MBench, _**with over a 9% improvement**_ in English evaluations and _**more than a 20% improvement**_ in Arabic evaluations. Furthermore, it excels in medical Visual Question Answering, Report Generation, and Report Summarization tasks.

---

## 📊 Model Performance
### BiMed-MBench Evaluation
![llavamed_spider](https://github.com/user-attachments/assets/88d1cee5-8848-43de-a830-394ff8a81a36)
### Clinical LLM Evaluation
![lmeval_sota](https://github.com/user-attachments/assets/ec35ae1b-bae8-4777-bf6d-cfe8fda0a7f0)

---

## ֎ BiMediX2 Architecture
![Bimedix2_arch](https://github.com/user-attachments/assets/b1b92056-629b-40d3-9a46-6b8373bce994)

---

## 🌟 Examples

![en1](https://github.com/user-attachments/assets/914e458b-3b47-441f-adc3-4fc6bc52f846)
![Example 2](assets/example2.png)
![bi1](https://github.com/user-attachments/assets/e54403be-8ba6-4670-922e-c189150a1168)
![multidomain](https://github.com/user-attachments/assets/f88c4c2e-668d-4247-8b78-f6e49f2d2484)

---

## 📜 License & Citation 

BiMediX2 is released under the CC-BY-NC-SA 4.0 License. For more details, please refer to the [LICENSE](https://github.com/mbzuai-oryx/BiMediX/blob/main/LICENSE.txt) file included in our BiMediX repository.    

⚠️ **Warning! This release, intended for research, is not ready for clinical or commercial use.**    


Users are urged to employ BiMediX2 responsibly, especially when applying its outputs in real-world medical scenarios. It is imperative to verify the model's advice with qualified healthcare professionals and not rely on it for medical diagnoses or treatment decisions. Despite the overall advancements BiMediX2 shares common challenges with other language models, including hallucinations, toxicity, and stereotypes. BiMediX2's medical diagnoses and recommendations are not infallible.

If you use BiMediX2 in your research, please cite our work as follows:  

```
@misc{mullappilly2024bimedix2biomedicalexpertlmm,
      title={BiMediX2: Bio-Medical EXpert LMM for Diverse Medical Modalities}, 
      author={Sahal Shaji Mullappilly and Mohammed Irfan Kurpath and Sara Pieri and Saeed Yahya Alseiari and Shanavas Cholakkal and Khaled Aldahmani and Fahad Khan and Rao Anwer and Salman Khan and Timothy Baldwin and Hisham Cholakkal},
      year={2024},
      eprint={2412.07769},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2412.07769}, 
}
```
---
## 🙏 Acknowledgements
We are thankful to [Meta Llama](https://huggingface.co/meta-llama) for releasing their models and [LLaVa](https://github.com/haotian-liu/LLaVA), [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl?tab=readme-ov-file#axolotl), [LLaVA++](https://github.com/mbzuai-oryx/LLaVA-pp) for their open-source code contributions.

We would like to thank Dr. Omair Mohammed, Dr. Mohammed Zidan and Dr. Vishal Thomas Oommen for their contribution in verification of medical responses.

The computations were enabled by resources provided by *LUMI hosted by CSC (Finland)* and *LUMI consortium*, and by *Berzelius* resource provided by the *Knut and Alice Wallenberg Foundation at the NSC*.

We are grateful to the *Meta Llama Impact Innovation Awards* for recognizing BiMediX2, as one of the winners awarded in September 2024. This recognition highlights our commitment to advancing AI-driven healthcare solutions.

---
