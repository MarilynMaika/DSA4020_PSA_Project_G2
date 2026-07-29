# DSA4020_PSA_Project_G2

# Kenyan Multilingual PSA Machine Translation

**DSA 4020A — Natural Language Processing | Semester Project**
*Prepared under the supervision of Dr. Edward Ombui*

A proof-of-concept multilingual machine translation (MT) system for Kenyan Public Service
Announcements (PSAs) — translating between English/Kiswahili and selected under-resourced
indigenous languages, and deploying the result as a working demo.

---

## 1. Project Overview DSA4020_PSA_Project_G2

**Goal:** build a deployable digital public good that translates PSAs between English/Kiswahili
and under-resourced Kenyan languages — **Ekegusii** (Bantu), — demonstrating few-shot cross-lingual transfer learning on a curated,
domain-specific PSA dataset.

### What is a PSA?

> A Public Service Announcement is a short, clear, action-oriented — and sometimes urgent —
> message that informs, warns, or guides the public about something they should do (health
> measures, safety advisories, deadlines, disaster alerts). Tone is typically directive or
> advisory, and PSAs are usually produced without commercial intent by government agencies,
> NGOs, or media outlets.

**Examples:**
- *"IEBC reminds voters to verify their details via SMS."*
- *"Ministry of Health: Avoid unnecessary travel to Ebola hotspots."*

### Team & Tools
- **Team size:** 5 students
- **Duration:** 4 weeks
- **Stack:** Python (Hugging Face, pandas, BeautifulSoup, Selenium), MT evaluation libraries
  (BLEU/chrF/COMET/SacreBLEU), Streamlit/Gradio for deployment.

---

## 2. Sub-Objectives

| # | Sub-objective | Points |
|---|---|---|
| 1 | Curate a high-quality multilingual dataset (≥5,000 sentences per language pair) | 25 |
| 2 | Explore few-shot cross-lingual transfer using pre-trained models (mT5, NLLB, mBART, etc.) | 30 |
| 3 | Evaluate the model for accuracy and cultural appropriateness | 20 |
| 4 | Deploy the model as a digital public good | 15 |
| — | Overall quality, documentation & presentation | 10 |

---

## 3. Timeline & Milestones

### Week 1 — Data Collection & Curation *(Sub-objective 1)* 
- Identify and document ≥10 reliable sources (gov sites, X/Twitter, media archives, NGOs).
- Hybrid scraping pipeline (manual + automated; BeautifulSoup/Selenium; robots.txt & rate limits respected).
- Collect raw PSAs across Education, Health, Security, Agriculture, Governance.
- Structured dataset with columns: `PSA_ID, Domain, English, Kiswahili, Target Languages (placeholders), Source, Date, Metadata`.
- Initial cleaning: deduplication, language detection, relevance filtering.
- Reach ≥5,000 parallel sentences with basic validation.
- Submit Week 1 report (dataset summary stats, sample entries, challenges).

### Week 2 — Data Processing & EDA *(Sub-objectives 1 & 2)*
- Preprocessing pipeline (tokenization, normalization, code-switching handling, cultural-term glossary).
- Full EDA: domain distribution, text length histograms, vocabulary size, language-pair stats.
- Native-speaker validation subset (~500 sentences) + feedback.
- Version-controlled cleaned dataset; train/dev/test splits.

### Week 3 — Modeling with Transfer Learning *(Sub-objective 2)*
- Experiment tracking (Weights & Biases / MLflow).
- ≥2 pre-trained models fine-tuned few-shot (e.g. mT5-small, NLLB-200 distilled, mBART).
- Low-resource training techniques (layer freezing, data augmentation); ablations (zero-shot vs. few-shot, domain adaptation).
- Inference script + preliminary performance summary.

### Week 4 — Evaluation, Deployment & Documentation *(Sub-objectives 3 & 4)*
- Automatic metrics (BLEU, chrF, COMET, SacreBLEU) + human evaluation (fluency, adequacy, cultural accuracy) on 100+ sentences.
- Error analysis and documented limitations.
- Web app deployment (Streamlit/Gradio): input PSA → select target language → output translation, with confidence scores and a feedback form.
- Final GitHub repo (code, dataset/link, notebooks, README, license) + final report + demo day.

---

## 4. PSA Domain Taxonomy

Every PSA is labeled with one of 5 domains and one of 5 sub-categories each (25 combinations total):

| Domain | Sub-Categories |
|---|---|
| **Health** | Disease Prevention & Control · Maternal & Child Health · Public Health Campaigns · Mental Health Awareness · Healthcare Access |
| **Agriculture** | Crop Production · Livestock Management · Agribusiness & Market Access · Sustainable Farming · Agricultural Training |
| **Education** | Access to Education · Vocational Training · Civic Education · Educational Resources · School Safety & Inclusion |
| **Security & Safety** | Public Safety Awareness · Crime Prevention · National Security · Gender-Based Violence · Cybersecurity |
| **Governance** | Anti-Corruption Initiatives · Public Participation · Elections & Voter Education · Public Service Delivery · Devolution & Local Governance |

---

## 5. Repository Structure

```
psa_pipeline/
├── README.md                          # pipeline-level documentation
├── requirements.txt
├── src/
│   ├── config.py                      # taxonomy, counties, paths, targets (single source of truth)
│   ├── mine_source.py                 # Step 1: mine authorities & phrasing from merged scrape
│   ├── templates.py                   # hand-authored PSA templates (25 domain x sub-category sets)
│   ├── generate.py                    # Step 2: fill templates -> synthetic PSAs
│   ├── dedup.py                       # Step 3: exact + fuzzy dedup (rapidfuzz)
│   ├── quality_check.py               # Step 4: rule-based cleanup & validation
│   └── pipeline.py                    # orchestrates Steps 1-4 end-to-end
├── data/
│   ├── merged_psa_dataset.csv         # combined team scrape (raw curation deliverable)
│   └── mined/                         # authorities.json, phrases.json, reference_lines.json
└── output/
    ├── kenyan_psa_synthetic_15000.csv # final synthetic dataset
    └── quality_report.txt
```

---

## 6. Current Status: 

- Data Collection

- Data Cleaning

- EDA

- Initial Finetuning Done!

Individual scraping efforts fell short of the 5,000-sentence target on their own, so the team
combined every member's output into one **merged scraped dataset**, then built a pipeline to
**mine that data for real Kenyan authorities and phrasing** and use them to generate a large,
clean **synthetic dataset** grounded in that real-world material.

### Merged Scraped Dataset (`data/merged_psa_dataset.csv`)
- **6,236 rows** across 11 columns: `PSA_ID, Domain, English, Kiswahili, Ekegusii, Somali, Dholuo, Target_Languages, Source, Date, Metadata`
- **1,178 distinct sources** — government sites, media wires, NGOs, official corpora
- Domain split: Education 1,852 · Agriculture 1,691 · Security & Safety 983 · Governance 937 · Health 773
- Kiswahili filled for 69.5% of rows; Ekegusii/Somali/Dholuo partially filled (placeholders, pending translation)

###  Synthetic Dataset (`output/kenyan_psa_synthetic_15000.csv`)
- **15,000 rows**, columns: `PSA_ID, Domain, English`
- 100% unique `English` text and `PSA_ID`; zero nulls
- Generated by mining real Kenyan issuing authorities and PSA phrasing patterns out of the
  merged scrape, then filling hand-authored templates with those authorities plus counties,
  months, and topics — followed by dedup and rule-based quality checks
### Final Merged Dataset used(Synthetic + Real)
- ~21306 rows final merged dataset(Bootstrapped synthetic + Real Scrapped(By group members + Provided by the lecturer)) Hybrid :`PSA_ID, Domain, English,Kswahili,Ekeguisi`
- Used LLM-based translation to Ekeguisi with fewshot
- Done Manual validation from Ekeguisi Speakers
### Pipeline Architecture

![Pipeline architecture](assets/architecture.png)

Parallel member scraping → merge → mine real authorities/phrasing → fill authored templates →
generate → dedup (exact + fuzzy) → rule-based quality check → final synthetic dataset. The
pipeline automatically tops up generation if dedup/QC drop the row count below 70,000.




### EDA Findings
### PSA Count by Domain

The chart illustrates the number of Public Service Announcements (PSAs) across different domains. For reporting purposes, **Security** and **Security & Safety** have been combined into a single category.

| Domain | PSA Count |
|---------|----------:|
| Education | 5,300 |
| Agriculture | 4,500 |
| Health | 4,100 |
| Security (Security + Security & Safety) | 4,000 |
| Governance | 3,500 |

**Summary**

- **Education** has the highest number of PSAs (5,300), indicating the greatest emphasis among all domains.
- **Agriculture** follows with approximately **4,500** PSAs.
- **Health** contains about **4,100** PSAs, making it one of the most represented domains.
- After combining **Security** (1,000) and **Security & Safety** (3,000), the **Security** category totals **4,000** PSAs.
- **Governance** has the lowest count among the merged categories, with approximately **3,500** PSAs.

Overall, the distribution shows that educational content dominates the dataset, while Agriculture, Health, and Security also receive substantial attention. Governance has comparatively fewer PSAs.

## Finetuning

Both fewshot and zeroshot.

Used Models:

 -mt5
 
 -NLLB

---

## 7. Running the Pipeline

```bash
cd src
pip install -r ../requirements.txt
python3 pipeline.py
```

To re-run an individual step (e.g. after editing `templates.py`):
```bash
python3 mine_source.py     # only needed if merged_psa_dataset.csv changes
python3 generate.py
python3 dedup.py
python3 quality_check.py
```

**Requires:** `pandas`, `numpy`, `rapidfuzz`.

---

### Challenges Faced

- **Limited GPU Resources**
  - Training and fine-tuning transformer-based models required significant computational power.
  - Limited GPU availability increased training time and restricted experimentation with larger models and hyperparameter tuning.

- **API Key Limitations for Few-Shot Ekegusii Translation**
  - The translation pipeline relied on external APIs for few-shot translation into Ekegusii.
  - API usage quotas, rate limits, and associated costs constrained the number of translation requests that could be made during dataset preparation.

- **Manual Validation by Native Ekegusii Speakers**
  - Since automated evaluation tools for Ekegusii are limited, translated texts had to be manually validated by native speakers.
  - This process was time-consuming and required careful review to ensure linguistic accuracy, cultural appropriateness, and consistency across the dataset.


## License

To be finalized for the Week 4 deliverable (e.g. CC-BY).
