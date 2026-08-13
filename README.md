# Kenyan PSA Machine Translation — English/Kiswahili → Ekegusii

**DSA 4020A — Natural Language Processing | Semester Project**
*Prepared under the supervision of Dr. Edward Ombui*

---

## 1. Project Overview

This project builds a proof-of-concept, deployable machine translation system for Kenyan Public Service Announcements (PSAs), translating from **English and Kiswahili into Ekegusii** — a Bantu language spoken by roughly 2.2 million people that has **no coverage at all** in the pretraining data of either model we fine-tuned. The end deliverable is a working public demo, built on top of two fine-tuned transformer models, developed across four weeks: data curation, processing and EDA, transfer-learning-based modeling, and evaluation/deployment.

> **What is a PSA?** A Public Service Announcement is a short, clear, action-oriented — and sometimes urgent — message that informs, warns, or guides the public about something they should do (health measures, safety advisories, deadlines, disaster alerts). PSAs are typically produced without commercial intent by government agencies, NGOs, or media outlets, and their tone is usually directive or advisory.

### Team & Tools
- **Team:** Ian Karugu, Queen Kibegi, Sevidzem Marilyn, Sylvia Njane, Hana Gashaw
- **Duration:** 4 weeks
- **Stack:** Python (Hugging Face `transformers`, `datasets`, `accelerate`, pandas, BeautifulSoup, Selenium), MLflow (experiment tracking), sacrebleu/`evaluate` (BLEU, chrF), Streamlit (deployment)

### Sub-Objectives

| # | Sub-objective | Points |
|---|---|---|
| 1 | Curate a high-quality multilingual dataset (≥5,000 sentences per language pair) | 25 |
| 2 | Explore few-shot cross-lingual transfer using pre-trained models (mT5, NLLB, mBART, etc.) | 30 |
| 3 | Evaluate the model for accuracy and cultural appropriateness | 20 |
| 4 | Deploy the model as a digital public good | 15 |
| — | Overall quality, documentation & presentation | 10 |

---

## 2. Repository Structure

```
DSA4020_PSA_Project_G2/
├── README.md                                    ← you are here
├── Week1_ Data Collection & Curation/
│   ├── Sources Used for Data Collection.docx     ← ≥10 documented sources
│   ├── Week1_Report.docx                         ← dataset summary, samples, challenges
│   └── hybrid_scraping_pipeline/
│       ├── Scrapping_manual_hybrid/              ← manual + automated scraping (src/, raw datasets)
│       └── psa_bootstrapped_generation_pipeline/ ← synthetic PSA generation (mining → templates → dedup → QC)
├── Week2_ DataProcessing&EDA/
│   ├── Final_merged_psas.csv                     ← final ~21K-row dataset used for modeling
│   ├── cultural_term_glossary.csv
│   ├── merge_psas.py
│   ├── psa_preprocessing_eda.ipynb               ← preprocessing + full EDA
│   └── train.csv / val.csv / test.csv            ← modeling splits
├── Week3_ModelingwithTransferLearning/
│   ├── training/                                 ← mt5_training.ipynb, nllb_training.ipynb
│   ├── logs/                                      ← per-model results, hyperparameters, domain ablation, predictions
│   ├── experiment_tracking/                       ← mlflow.db, mlruns/ (MLflow tracking)
│   ├── GPU&Environment_troubleshooting.docx
│   └── requirements.txt
└── Week4_ Evaluation,Deployment&Documentation/
    ├── mt5_evaluation.ipynb / nllb_evaluation.ipynb
    ├── Error Analysis and Limitations.docx
    ├── Human_Evaluation.docx
    └── deployment/                                ← app.py, requirements.txt, upload_models.py, access_the_app.docx
```

---

## 3. Week 1 — Data Collection & Curation *(Sub-objective 1)*

**Goal:** a parallel dataset of ≥5,000 sentences, hybrid-sourced and structured for downstream modeling.

- **Sources documented:** ≥10 reliable sources across government sites, media archives, and NGOs (see `Sources Used for Data Collection.docx`).
- **Hybrid scraping pipeline:** manual + automated collection (BeautifulSoup/Selenium), respecting `robots.txt` and rate limits — see `hybrid_scraping_pipeline/Scrapping_manual_hybrid/`.
- **Raw scrape:** individual member scraping efforts combined into a **merged dataset of 6,236 rows**,spanning Education, Agriculture, Security & Safety, Governance, and Health.
- **Synthetic augmentation:** rather than stopping at the raw scrape, a second pipeline (`psa_bootstrapped_generation_pipeline/`) mined real Kenyan issuing authorities and PSA phrasing patterns from the merged scrape, then used them to fill hand-authored templates across all 25 domain × sub-category combinations — generating a **synthetic dataset of 15,000 rows**, deduplicated (exact + fuzzy matching) and rule-checked for quality.

### PSA Domain Taxonomy

Every PSA is labeled with one of 5 domains, each with 5 sub-categories (25 combinations total):

| Domain | Sub-Categories |
|---|---|
| **Health** | Disease Prevention & Control · Maternal & Child Health · Public Health Campaigns · Mental Health Awareness · Healthcare Access |
| **Agriculture** | Crop Production · Livestock Management · Agribusiness & Market Access · Sustainable Farming · Agricultural Training |
| **Education** | Access to Education · Vocational Training · Civic Education · Educational Resources · School Safety & Inclusion |
| **Security & Safety** | Public Safety Awareness · Crime Prevention · National Security · Gender-Based Violence · Cybersecurity |
| **Governance** | Anti-Corruption Initiatives · Public Participation · Elections & Voter Education · Public Service Delivery · Devolution & Local Governance |

### Final Dataset — Domain Distribution (21,306 rows)

| Domain | PSA Count | Share |
|---|--:|--:|
| Education | 5,300 | 24.8% |
| Agriculture | 4,500 | 20.9% |
| Health | 4,100 | 19.2% |
| Security & Safety | 4,000 | 18.8% |
| Governance | 3,500 | 16.2% |

### Sample Entries

| PSA ID | Domain | English PSA |
|--:|---|---|
| 1 | Agriculture | Farmers are urged to prioritize safe agrochemical usage as Kenya hosts the World Farmers' Organisation General Assembly. |
| 2 | Agriculture | Trucks ferrying top-dressing fertilizer are now arriving at the Eldoret Depot of the National Cereals and Produce Board. Farmers are encouraged to collect their supplies. |
| 3 | Agriculture | Farmers in Wajir are invited to participate in the KSh. 5 billion Livestock Investment Drive launched by President Ruto. |


**Ekegusii translation:** LLM-based, few-shot-prompted translation from English/Kiswahili into Ekegusii, followed by **manual validation from native Ekegusii speakers**.

---

## 4. Week 2 — Data Processing & EDA *(Sub-objectives 1 & 2)*

- **Preprocessing pipeline** (`psa_preprocessing_eda.ipynb`): tokenization, normalization, code-switching handling, and a dedicated **cultural-term glossary** (`cultural_term_glossary.csv`) for domain-specific vocabulary that doesn't translate literally.
- **EDA:** domain distribution, text length distributions, vocabulary size, and language-pair statistics across the full 21,306-row dataset (see table above).
- **Native-speaker validation:** a subset reviewed by native Ekegusii speakers to sanity-check translation quality ahead of modeling.
- **Modeling splits:** `train.csv`, `val.csv`, `test.csv` — split by **unique PSA identifier** (not by row) to prevent the English and Kiswahili versions of the same PSA from leaking across train/test, since both map to the same Ekegusii target.

---

## 5. Week 3 — Modeling with Transfer Learning *(Sub-objective 2)*

Two pretrained multilingual transformer models were fine-tuned on the curated dataset:

| | mT5-small | NLLB-200-distilled-600M |
|---|---|---|
| **Conditioning** | Task-prefix in the input text (`"translate English to Ekegusii: "`) | Tokenizer-level target-language tag (Ekegusii has no native NLLB code, so a placeholder tag is used) |
| **Low-resource technique** | 4 of 8 encoder layers frozen | 6 of 12 encoder layers frozen |
| **Precision** | fp32 (fp16 causes NaN losses on mT5) | bf16-capable |
| **Epochs** | 5, best checkpoint selected by validation BLEU | 5, best checkpoint selected by validation BLEU |
| **Optimizer** | AdamW | AdamW |
| **Training time** | ~90 minutes (single A100 80GB GPU) | ~90 minutes (single A100 80GB GPU) |

**Experiment tracking:** all runs tracked via MLflow (`experiment_tracking/mlflow.db`, `mlruns/`) — per-epoch loss/BLEU/chrF, hyperparameters, and training time logged automatically.

### Ablation: Zero-shot vs. Few-shot

| Model | Direction | Zero-shot BLEU | Zero-shot chrF | Few-shot BLEU | Few-shot chrF |
|---|---|--:|--:|--:|--:|
| mT5-small | English→Ekegusii | 0.005 | 1.18 | 3.08 | 25.79 |
| mT5-small | Kiswahili→Ekegusii | 0.013 | 1.44 | 2.69 | 24.57 |
| NLLB-200 | English→Ekegusii | 5.58 | 22.88 | 3.49 | 25.27 |
| NLLB-200 | Kiswahili→Ekegusii | 6.46 | 24.24 | 3.08 | 25.20 |

mT5's chrF improved roughly **20×** (1.2 → ~25) from zero-shot to few-shot — strong evidence of genuine Ekegusii acquisition, since mT5 had zero prior exposure to the language. NLLB's zero-shot chrF starts much higher (likely cross-lingual transfer via its placeholder tag), but its **few-shot BLEU is lower than its own zero-shot BLEU** — see Section 6 for why this is not a regression in practice.

A **domain-level ablation** (per-domain BLEU/chrF across the five PSA categories) is also included in `logs/*_domain_ablation.csv` for both models.

### GPU & Environment Troubleshooting (Mid-week check-in)

Two infrastructure issues required troubleshooting before training could proceed cleanly:

Our first obstacle wasn't a code issue but an infrastructure misconfiguration: our compute environment had initially been provisioned in "Serverless" mode rather than pointed at our team's dedicated GPU grid, meaning no GPU was actually attached to the container despite the physical node having an NVIDIA A100 80GB available. This was diagnosed by running `nvidia-smi` inside the running app and receiving a "command not found" error, alongside confirming no `/dev/nvidia*` device files existed inside the container. The fix required explicitly targeting the existing GPU grid in the app's resource configuration, after which `nvidia-smi` correctly reported the attached A100.

A second issue arose once training began: a `RuntimeError: Failed to find C compiler` was raised by PyTorch's Triton backend, which attempts to just-in-time compile certain attention operations and requires a system-level C compiler unavailable in our minimal base image. This was resolved by pinning an older PyTorch version to avoid the Triton compilation path entirely, with one further version adjustment required to satisfy a `transformers` security check (CVE-2025-32434) mandating PyTorch ≥2.6 for safe checkpoint loading. Full details in `GPU&Environment_troubleshooting.docx`.

**Models on the Hugging Face Hub:**
- mT5: [`HanaHailemariam/mt5-en-guz`](https://huggingface.co/HanaHailemariam/mt5-en-guz)
- NLLB: [`HanaHailemariam/nllb-en-guz`](https://huggingface.co/HanaHailemariam/nllb-en-guz)

---

## 6. Week 4 — Evaluation, Deployment & Documentation *(Sub-objectives 3 & 4)*

### Error Analysis

Manual inspection of model outputs — not aggregate metrics alone — surfaced two distinct failure modes:

1. **mT5 repetition under greedy decoding.** On some inputs, mT5 entered a degenerate loop, repeating the same short phrase until hitting the maximum generation length. This was a decoding-strategy issue, not a training problem, and was resolved by switching from greedy decoding to **beam search** (`num_beams=4`) with `no_repeat_ngram_size` and `repetition_penalty` constraints.

2. **NLLB defaulting to Kiswahili instead of Ekegusii.** Root-cause analysis traced this to a preprocessing defect: the tokenizer's target-language state was never explicitly set during label tokenization, so training labels were inconsistently tagged rather than consistently marked as Ekegusii. Combined with NLLB's strong pretrained association between the placeholder tag (borrowed from Kiswahili) and genuine Kiswahili, the model defaulted toward its pretrained behavior at generation time. **This was fixed** by explicitly setting `tokenizer.tgt_lang` before encoding every training label, and the model was retrained.

   Interestingly, the retrained model's few-shot BLEU is *lower* than the original buggy run's (see the ablation table above) — we believe this reflects the earlier run's output being fluent **Kiswahili**, which shares enough vocabulary with the closely related Bantu language Ekegusii to score deceptively well against the reference on exact n-gram overlap, despite being the wrong language. The corrected model's lower BLEU alongside comparable chrF is consistent with it producing genuinely different, non-Kiswahili output — this is discussed further with the course instructor, at whose suggestion the retrain was carried out.

### Human Evaluation (Preliminary)

Ahead of a full structured evaluation, informal feedback was solicited from a native Ekegusii-speaking member of the course teaching staff, at two points:

- **Before the fix:** translations were reported as not usable — beyond the literal repetition loops, even non-looping outputs did not read as coherent Ekegusii; words appeared disconnected from the source sentence's meaning.
- **After the fix:** the same reviewer reported a clear improvement — outputs no longer repeated, and vocabulary was recognizably Ekegusii, generally staying relevant to the source sentence's topic. The reviewer was clear this is not yet fluent: sentence structure and grammatical coherence remain inconsistent, and a full, larger-scale (100+ sentence) structured human evaluation is planned as a next step.

Full write-up in `Human_Evaluation.docx` and `Error Analysis and Limitations.docx`.

### Limitations

- Structured human evaluation with native speakers across 100+ sentences has not yet been completed; current native-speaker feedback is preliminary and qualitative.
- NLLB's reliance on a repurposed placeholder language tag (rather than a dedicated Ekegusii token) remains an architectural constraint that preprocessing fixes mitigate but cannot fully eliminate.
- Absolute translation quality remains modest (chrF in the low-to-mid 20s), reflecting the genuine scarcity of parallel Ekegusii training data rather than a flaw specific to either model.
- Shared, constrained GPU access limited the number of full training iterations and hyperparameter sweeps feasible within the project timeline.
- The public demo's free-tier hosting has a memory ceiling that required removing a "compare both models side by side" mode, so the live app currently serves one model per translation request.

### Deployment

The fine-tuned models are served through a public **Streamlit** web app: paste a PSA, pick a source language (English or Kiswahili), select a model, and get an Ekegusii translation.

- **Live demo:**(https://psa-translation-jq7jgyyhuftkghnzggjum7.streamlit.app/)

  > *Note: If you're trying the app after a period of inactivity, it may have gone to sleep to conserve hosting resources. It usually wakes up on its own within about a minute — try refreshing if it doesn't load right away. If it's still unresponsive after that, feel free to email [21ibtj@gmail.com](mailto:21ibtj@gmail.com) and we'll wake it back up so you can try your translations.*

- **Deployment source:** [`ibtj21/psa-translation`](https://github.com/ibtj21/psa-translation) (companion repo connected to the live Streamlit deployment; a copy of the same code is included here under `Week4_ Evaluation,Deployment&Documentation/deployment/`)

**App features:**
- Example PSA picker, drawing real sentences from the held-out test set
- Source language selector (English / Kiswahili); target language is fixed to Ekegusii
- Model selector (mT5-small / NLLB-200-distilled-600M), with an inline note on NLLB's known Kiswahili-leakage limitation
- Per-translation confidence score (mean token probability), explicitly labeled as a rough signal rather than a guarantee
- Feedback form (Good / Needs work + optional comment), stored locally and not shared elsewhere

---

## 7. License

This project is released under the **MIT License**. See `LICENSE` for full terms.

---

## 8. Challenges Faced

- **Limited GPU resources** — training and fine-tuning transformer models required significant compute; shared/limited GPU access increased training time and constrained experimentation with larger models or more extensive hyperparameter tuning.
- **API limitations for few-shot Ekegusii translation** — the initial LLM-based translation pipeline relied on external APIs, whose usage quotas and rate limits constrained how many translation requests could be made during dataset preparation.
- **Manual validation by native Ekegusii speakers** — with limited automated evaluation tooling for Ekegusii, translated text required time-consuming manual review to check linguistic accuracy and cultural appropriateness.
- **Infrastructure and dependency troubleshooting** — GPU provisioning misconfigurations and a chain of PyTorch/CUDA version compatibility issues (detailed in Section 5) required systematic debugging before full-scale training could proceed.
