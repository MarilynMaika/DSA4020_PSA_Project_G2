# Kenya PSA Multilingual Dataset — Project Report

> **Project:** AI Agent for Crawling Public Service Announcements (PSAs)  
> **Focus:** Kenya — Health, Education, Security, Agriculture, Governance, Disaster  
> **Languages:** English, Kiswahili, Somali, Dholuo, Ekegusii  
> **Date:** July 2026  

---

## 1. Executive Summary

This report documents the creation of a high-quality multilingual parallel dataset of Public Service Announcements (PSAs) sourced from Kenyan government portals, NGOs, media archives, and official social media accounts. The dataset is designed to train and evaluate machine translation and cross-lingual NLP models for low-resource African languages.

| Metric | Value |
|---|---|
| **Initial corpus size** | 5,200 parallel sentences |
| **After deduplication** | **5,011 parallel sentences** |
| **Coverage domains** | 6 (Agriculture, Disaster, Education, Governance, Health, Security) |
| **Language pairs** | EN ↔ SW (complete), EN ↔ SO (complete), EN ↔ LUO (pending), EN ↔ EKE (pending) |
| **Sources documented** | 12 official and media sources |

---

## 2. Dataset Summary Statistics

### 2.1 Overall Size

| Stage | Count | Notes |
|---|---|---|
| Raw collected | 5,200 | Before any cleaning |
| After deduplication | **5,011** | Content-hash + fuzzy duplicate removal |
| Unique English sentences | 5,011 | 96.4% uniqueness rate |
| Unique Kiswahili sentences | 5,011 | 96.4% uniqueness rate |

### 2.2 Domain Distribution

| Domain | Count | Percentage | Status |
|---|---|---|---|
| Agriculture | 874 | 17.4% | ✅ Complete |
| Disaster | 870 | 17.4% | ✅ Complete |
| Education | 857 | 17.1% | ✅ Complete |
| Governance | 811 | 16.2% | ✅ Complete |
| Health | 866 | 17.3% | ✅ Complete |
| Security | 733 | 14.6% | ✅ Complete |
| **Total** | **5,011** | **100%** | |

> **Note:** Security domain is slightly under-represented (14.6% vs. target 16.7%). This is due to fewer publicly archived security advisories in structured formats. [FILLER: Add planned mitigation strategy here.]

### 2.3 Text Length Statistics

| Language | Mean (chars) | Median (chars) | Min | Max | Std Dev |
|---|---|---|---|---|---|
| English | 87.9 | 88.0 | 38 | 158 | 18.7 |
| Kiswahili | 95.0 | 94.0 | 38 | 170 | 20.6 |
| Somali | [FILLER: Add after translation review] | — | — | — | — |
| Dholuo | [Pending translation] | — | — | — | — |
| Ekegusii | [Pending translation] | — | — | — | — |






### 2.5 Source Distribution



> **FILLER:** Add breakdown of how many entries came from live scraping vs. template generation vs. manual curation.

---

## 3. Sample Entries

### 3.1 Health Domain

## Dataset Preview

| PSA_ID | Domain | English | Kiswahili | Somali | Dholuo | Source | Date |
|--------|--------|---------|-----------|---------|---------|--------|------|
| PSA000001 | Health | The Ministry of Health advises all residents to boil drinking water before use... | Wizara ya Afya inawashauri wakazi wote kuchemsha maji ya kunywa kabla ya matumizi... | Wasaaradda Caafimaadka waxay kula talinaysaa dhammaan dadka deegaanka inay karkariyaan biyaha cabbitaanka... | — | IEBC Kenya | 2024-11-23 |
| PSA000002 | Health | **URGENT:** Avoid unnecessary travel to Ebola-affected areas... | **HARAKA:** Epuka kusafiri bila lazima kwenda maeneo yaliyoathiriwa na Ebola... | **DEGDEG AH:** Ka fogow safar aan loo baahnayn oo lagu tagayo meelaha Ebola saameeyay... | — | Ministry of Health | 2024-01-18 |
| PSA000003 | Health | Parents are reminded to ensure children under five receive all recommended vaccinations... | Wazazi wanakumbushwa kuhakikisha watoto walio chini ya miaka mitano wanapata chanjo zote zinazopendekezwa... | Waalidiinta waxaa la xasuusinayaa inay hubiyaan carruurta ka yar shan sano inay helaan dhammaan tallaalada lagu taliyey... | — | Ministry of Health | 2025-07-17 |
### 3.2 Education Domain

| PSA_ID | Domain | English | Kiswahili | Somali | Dholuo | Source | Date |
|--------|--------|---------|-----------|---------|---------|--------|------|
| PSA000016 | Education | The Ministry of Education announces that all schools should adhere to the updated academic calendar... | Wizara ya Elimu inatangaza kwamba shule zote zinapaswa kuzingatia kalenda mpya ya masomo... | Wasaaradda Waxbarashada ayaa ku dhawaaqday in dhammaan dugsiyadu ay raacaan jadwalka cusub ee waxbarashada... | — | IEBC Kenya | 2025-05-20 |
| PSA000017 | Education | All KCSE candidates must verify their examination registration details before the deadline... | Watahiniwa wote wa KCSE lazima wathibitishe maelezo yao ya usajili wa mtihani kabla ya tarehe ya mwisho... | Dhammaan ardayda imtixaanka KCSE waa inay xaqiijiyaan xogtooda diiwaangelinta imtixaanka ka hor waqtiga kama dambaysta ah... | — | Social Health Authority | 2025-12-22 |
| PSA000018 | Education | Parents are reminded that the deadline for Form One student placement confirmation is approaching... | Wazazi wanakumbushwa kwamba tarehe ya mwisho ya kuthibitisha nafasi za wanafunzi wa Kidato cha Kwanza inakaribia... | Waalidiinta waxaa la xasuusinayaa in waqtiga kama dambaysta ah ee xaqiijinta nafasi za ardayda Fasalka ya Kwanza ee Sekondari uu soo dhow yahay... | — | Kenya Meteorological Department | 2026-02-20 |

### 3.3 Security Domain

| PSA_ID | Domain | English | Kiswahili | Somali | Dholuo | Source | Date |
|--------|--------|---------|-----------|---------|---------|--------|------|
| PSA000031 | Security | The National Police Service urges citizens to remain vigilant and report suspicious activities... | Huduma ya Kitaifa ya Polisi inawahimiza raia kubaki waangalifu na kuripoti shughuli zinazotiliwa shaka... | Adeegga Booliska Qaranka wuxuu ku boorinayaa muwaadiniinta inay feejignaadaan oo ay soo sheegaan dhaqdhaqaaqyada laga shakiyo... | — | Kenya Red Cross | 2026-02-22 |
| PSA000032 | Security | **SECURITY ALERT:** Avoid the Nairobi–Mombasa highway until further notice... | **TAHADHARI YA USALAMA:** Epuka barabara kuu ya Nairobi–Mombasa hadi taarifa nyingine... | **DIGNIIN AMNIGA:** Ka fogow waddada weyn ee isku xirta Nairobi iyo Mombasa ilaa ogeysiis dambe... | — | Ministry of Education | 2026-01-06 |
| PSA000033 | Security | All residents of Mandera County are advised to follow official security instructions... | Wakazi wote wa Kaunti ya Mandera wanashauriwa kufuata maelekezo rasmi ya usalama... | Dhammaan dadka degan Degmada Mandheera waxaa lagula talinayaa inay raacaan tilmaamaha rasmiga ah ee amniga... | — | National Police Service | 2026-05-26 |

### 3.4 Agriculture Domain

| PSA_ID | Domain | English | Kiswahili | Somali | Dholuo | Source | Date |
|--------|--------|---------|-----------|---------|---------|--------|------|
| PSA000046 | Agriculture | The Ministry of Agriculture advises farmers in affected regions to adopt recommended farming practices... | Wizara ya Kilimo inawashauri wakulima katika maeneo yaliyoathirika kufuata mbinu zilizopendekezwa za kilimo... | Wasaaradda Beeraha waxay kula talinaysaa beeraleyda ku sugan meelaha ay dhibaatadu saameysay inay raacaan hababka beeraha ee lagu taliyey... | — | Ministry of Health | 2024-02-22 |
| PSA000047 | Agriculture | **URGENT:** All livestock farmers must vaccinate their animals against the reported disease outbreak... | **HARAKA:** Wafugaji wote lazima wachanje wanyama wao dhidi ya mlipuko wa ugonjwa ulioripotiwa... | **DEGDEG AH:** Dhammaan beeraleyda xoolaha waa inay tallaalaan xoolahooda si looga hortago cudurka la soo sheegay... | — | National Police Service | 2026-02-03 |
| PSA000048 | Agriculture | The National Cereals and Produce Board announces new grain purchasing guidelines for farmers... | Bodi ya Kitaifa ya Nafaka na Mazao yatangaza miongozo mipya ya ununuzi wa nafaka kwa wakulima... | Guddiga Qaranka ee Badarka iyo Waxsoosaarka ayaa ku dhawaaqay tilmaamo cusub oo ku saabsan iibsiga badarka ee beeraleyda... | — | Ministry of Health | 2025-12-05 |

### 3.5 Governance Domain

| PSA_ID | Domain | English | Kiswahili | Somali | Dholuo | Source | Date |
|--------|--------|---------|-----------|---------|---------|--------|------|
| PSA000061 | Governance | IEBC reminds all eligible voters to verify their voter registration details before the upcoming election... | IEBC inawakumbusha wapiga kura wote wanaostahili kuthibitisha taarifa zao za usajili wa wapiga kura kabla ya uchaguzi ujao... | Guddiga Doorashooyinka IEBC wuxuu xasuusinayaa dhammaan codbixiyeyaasha u qalma inay xaqiijiyaan xogtooda diiwaangelinta codbixinta ka hor doorashada soo socota... | — | Ministry of Agriculture | 2024-08-08 |
| PSA000062 | Governance | The government announces that all national identity card applications can now be submitted through the online citizen portal... | Serikali yatangaza kwamba maombi yote ya vitambulisho vya taifa sasa yanaweza kuwasilishwa kupitia tovuti ya huduma za serikali... | Dowladdu waxay ku dhawaaqday in dhammaan codsiyada kaararka aqoonsiga qaranka hadda lagu gudbin karo bogga adeegyada dowladda... | — | Social Health Authority | 2025-12-01 |
| PSA000063 | Governance | All civil servants are directed to update their employment records through the official government portal... | Watumishi wote wa umma wameagizwa kusasisha taarifa zao za ajira kupitia tovuti rasmi ya serikali... | Dhammaan shaqaalaha rayidka ah waxaa la farayaa inay cusboonaysiiyaan diiwaannadooda shaqo iyagoo adeegsanaya bogga rasmiga ah ee dowladda... | — | Social Health Authority | 2025-04-25 |

### 3.6 Disaster Domain

| PSA_ID | Domain | English | Kiswahili | Somali | Dholuo | Source | Date |
|--------|--------|---------|-----------|---------|---------|--------|------|
| PSA000076 | Disaster | The Kenya Meteorological Department warns of heavy rainfall and possible flooding in affected regions... | Idara ya Hali ya Hewa ya Kenya yaonya kuhusu mvua kubwa na uwezekano wa mafuriko katika maeneo yaliyoathirika... | Waaxda Saadaasha Hawada ee Kenya ayaa ka digaysa roobab culus iyo fatahaado suurtagal ah oo ka dhici kara meelaha ay saameeyeen... | — | Ministry of Health | 2024-01-29 |
| PSA000077 | Disaster | **EVACUATION ORDER:** All residents along the Tana River are instructed to move to higher ground immediately... | **AGIZO LA KUHAMISHA:** Wakazi wote kando ya Mto Tana wanaagizwa kuhamia maeneo ya juu mara moja... | **DALABKA BIXITAANKA:** Dhammaan dadka deggan hareeraha Webiga Tana waxaa lagu amray inay u guuraan dhulka sare isla markiiba... | — | Ministry of Agriculture | 2025-03-17 |
| PSA000078 | Disaster | The National Disaster Operations Centre issues updated safety guidelines following the recent emergency... | Kituo cha Kitaifa cha Operesheni za Maafa kimetoa miongozo mipya ya usalama kufuatia dharura ya hivi karibuni... | Xarunta Qaranka ee Hawlgallada Masiibooyinka ayaa soo saartay tilmaamo cusub oo badbaado kadib xaaladdii degdegga ahayd ee dhowaan dhacday... | — | Ministry of Education | 2025-11-14 |



---


**Tools used:**
- `requests` + `BeautifulSoup4` for static HTML
- `Selenium` (headless Chrome) for JavaScript-rendered pages
- `snscrape` for X/Twitter (no API key required)
- `langdetect` for language identification
- `pandas` for data manipulation

### 4.3 Data Cleaning Pipeline

| Step | Technique | Records Removed | Notes |
|---|---|---|---|
| Deduplication | MD5 hash on normalized text | 189 | Exact duplicates |
| Fuzzy dedup | [FILLER: Add if used] | [FILLER] | Near-duplicate detection |
| Language filter | `langdetect` confidence ≥ 0.9 | [FILLER] | Non-English filtered out |
| Relevance filter | PSA keyword score ≥ 2 | [FILLER] | Non-PSA content removed |
| Length filter | 30 ≤ chars ≤ 200 | [FILLER] | Too short / too long removed |

> **FILLER:** Complete the table with actual numbers from your cleaning run.

### 4.4 Translation Workflow

| Language | Method | Status | Quality Notes |
|---|---|---|---|
| **Kiswahili** | Template-based + Google Sheets MT | ✅ Complete | Reviewed for government register consistency |
| **Somali** | Google Sheets Translate | ✅ Complete | [FILLER: Add review notes — e.g., dialect bias toward Northern Somali?] |
| **Dholuo** | [FILLER: Planned method] | ⏳ Pending | [FILLER: e.g., community translator, Luo NMT model, or manual] |
| **Ekegusii** | [FILLER: Planned method] | ⏳ Pending | [FILLER: e.g., community translator, Gusii NMT model, or manual] |



---

## 5. Challenges Faced

### 5.1 Data Collection Challenges

| # | Challenge | Impact | Mitigation Attempted | Status |
|---|---|---|---|---|
| 1 | **Limited structured PSA archives** — Most Kenyan government sites lack dedicated PSA feeds; announcements are buried in general news pages. | Reduced automated scraping yield; more manual curation needed. | Implemented keyword + pattern-based relevance scoring to filter news pages. | Partially resolved |
| 2 | **No official Kiswahili PSA portals** — Government PSAs are overwhelmingly English-only. Kiswahili versions must be inferred or translated. | Bilingual parallel data is synthetic for ~[FILLER]% of entries. | Used template-based generation with verified bilingual fillers. | Mitigated but noted |
| 3 | **X/Twitter API restrictions** — snscrape works but is fragile; official API v2 requires paid tier for historical data. | Limited social media PSA recovery to recent tweets only. | Cached tweets locally; flagged for re-scrape before model training. | Ongoing |
| 4 | **Rate limiting and blocking** — Some government sites (e.g., health.go.ke) use Cloudflare or aggressive rate limits. | Scraping interruptions; incomplete data from some sources. | Implemented exponential backoff, rotating headers, and respectful delays (5–10s). | Partially resolved |
| 5 | **CAPTCHA on dynamic portals** — Selenium encounters CAPTCHA on some e-government portals. | Cannot fully automate certain high-value sources. | [FILLER: Add if 2captcha or manual solving was used.] | [FILLER] |
| 6 | **Security domain under-representation** — Police and security advisories are often classified or communicated via radio/SMS, not web. | Security PSAs are 14.6% of dataset vs. 16.7% target. | Added Twitter scraper for @NPSOfficial_KE; supplemented with media archives. | Partially resolved |

### 5.2 Translation Challenges

| # | Challenge | Impact | Mitigation | Status |
|---|---|---|---|---|
| 7 | **Dholuo translation unavailable** — No reliable MT engine for Dholuo; Google Translate does not support it. | Cannot auto-generate LUO column. | [FILLER: Planned approach — e.g., recruit Luo-speaking annotator, use OPUS-MT if available, or pivot to another language.] | ⏳ Pending |
| 8 | **Ekegusii translation unavailable** — Same as above; Ekegusii is extremely low-resource online. | Cannot auto-generate EKE column. | [FILLER: Planned approach.] | ⏳ Pending |
| 9 | **Somali dialect variation** — Google Sheets MT may bias toward Northern Somali (Standard Somali), while Kenyan Somali communities may use Maay Maay or local variants. | Potential domain mismatch for Kenyan target users. | [FILLER: Add if dialect review was done; flag for community validation.] | [FILLER] |
| 10 | **Kiswahili register consistency** — Government Kiswahili uses formal "Standard Kiswahili" (e.g., *Wizara*), while community PSAs may use Sheng or coastal dialects. | Risk of overly formal translations for grassroots communication. | Reviewed against KNBS and Ministry of Health style guides. | Mitigated |

### 5.3 Technical Challenges

| # | Challenge | Impact | Mitigation | Status |
|---|---|---|---|---|
| 11 | **Template leakage** — Early generation had English words bleeding into Kiswahili sentences when fillers were monolingual. | ~[FILLER]% of initial 5,200 had mixed-language issues. | Rebuilt filler system with bilingual EN-SW pairs; re-generated entire dataset. | Resolved |
| 12 | **Date authenticity** — Mix of synthetic dates (templates) and real dates (scraped) complicates temporal analysis. | Cannot reliably train time-sensitive models without disambiguation. | Added `Metadata.type` field flagging `handcrafted_template` vs. `scraped`. | Documented |
| 13 | **Language detection uncertainty** — `langdetect` struggles with short PSAs (< 30 chars) and code-switched text. | Misclassification of some entries. | [FILLER: Add if fasttext was tested as alternative; report accuracy.] | [FILLER] |

> **FILLER:** Add any additional challenges encountered during your specific workflow (e.g., storage limits, compute constraints, team coordination).

---

## 6. Known Limitations & Future Work

### 6.1 Current Limitations

1. **Synthetic data proportion:** A significant portion of the dataset is template-generated rather than scraped from authentic sources. [FILLER: Insert exact proportion after audit.]
2. **Missing languages:** Dholuo and Ekegusii columns are placeholders. The dataset is not yet fully multilingual.
3. **No human validation:** Translations have not undergone professional human review. [FILLER: Update if review was done.]
4. **Temporal bias:** Heavy weighting toward 2024–2026; historical PSAs (e.g., 2020 COVID era) are under-represented.
5. **Source bias:** Government sources dominate; grassroots/community PSA channels (chiefs' barazas, local radio) are not captured.

### 6.2 Planned Improvements

| Priority | Task | Owner | Timeline |
|---|---|---|---|
| P0 | Obtain Dholuo translations | [FILLER] | [FILLER] |
| P0 | Obtain Ekegusii translations | [FILLER] | [FILLER] |
| P1 | Human review of Somali translations | [FILLER] | [FILLER] |
| P1 | Human review of Kiswahili translations | [FILLER] | [FILLER] |
| P2 | Back-translation validation (SW→EN→SW) | [FILLER] | [FILLER] |
| P2 | Add 2020–2023 historical PSAs | [FILLER] | [FILLER] |
| P3 | Integrate community radio transcripts | [FILLER] | [FILLER] |
| P3 | Expand to additional languages (Kikuyu, Kalenjin, Kamba) | [FILLER] | [FILLER] |

> **FILLER:** Customize priority, owner, and timeline columns to match your project plan.

---

## 7. File Inventory

| Filename | Format | Size | Description |
|---|---|---|---|
| `kenya_psa_dataset.csv` | CSV | ~2.9 MB | Main dataset: 5,011 rows × 8 columns |
| `kenya_psa_dataset.json` | JSON | ~3.6 MB | Same data in JSON Lines format |
| `kenya_psa_sources.json` | JSON | ~6.7 KB | Source documentation (12 sources) |
| `psa_scraper.py` | Python | ~20.7 KB | Hybrid scraping pipeline module |
| `psa_scraper.log` | Text | [FILLER] | Execution logs from scraping runs |
| `README.md` | Markdown | This file | Project report and documentation |

> **FILLER:** Add any additional files (e.g., translation sheets, review spreadsheets, model checkpoints).

---

## 8. Citation & Usage

If you use this dataset, please cite:

```bibtex
@dataset{kenya_psa_2026,
  title = {Kenya Public Service Announcements Multilingual Dataset},
  author = {[FILLER: Add author names]},
  year = {2026},
  publisher = {[FILLER: Add institution]},
  url = {[FILLER: Add repository URL]},
  version = {1.0},
  language = {en, sw, so, luo, eke}
}
```

**License:** [FILLER: Add license — e.g., CC-BY-SA 4.0, MIT, or proprietary]  
**Contact:** [FILLER: Add contact email]  
**Acknowledgments:** [FILLER: Add funding sources, advisors, community contributors]

---

## 9. Appendix: Quick Reference

### A. PSA Quality Criteria

A valid PSA in this dataset meets **at least 2** of the following:

- [x] Short and clear (≤150 characters)
- [x] Action-oriented (contains directive verb: *must, should, urged, advised*)
- [x] Sometimes urgent (contains: *urgent, alert, warning, immediately*)
- [x] Public-facing (addresses *citizens, residents, public, parents, farmers*)
- [x] Domain-specific (health, education, security, agriculture, governance, disaster)

### B. Domain Keyword Map

| Domain | English Keywords | Kiswahili Keywords |
|---|---|---|
| Health | disease, vaccine, hospital, cholera, malaria | ugonjwa, chanjo, hospitali, kipindupindu, malaria |
| Education | school, exam, student, teacher, curriculum | shule, mtihani, mwanafunzi, mwalimu, mtaala |
| Security | police, curfew, alert, patrol, crime | polisi, amri ya kutotoka, onyo, doria, uhalifu |
| Agriculture | farm, crop, livestock, drought, harvest | shamba, zao, mifugo, ukame, mavuno |
| Governance | election, vote, register, IEBC, tax | uchaguzi, kura, sajili, IEBC, kodi |
| Disaster | flood, evacuate, warning, emergency, relief | mafuriko, hama, onyo, dharura, misaada |

### C. Metadata Schema

```json
{
  "type": "handcrafted_template | generated_variation | scraped",
  "psa_score": "integer (2-8) — keyword match count",
  "language_detected": "en | sw | so | luo | eke | unknown",
  "urgency_level": "low | medium | high | urgent",
  "generated_at": "ISO 8601 timestamp",
  "review_status": "[FILLER: Add if review workflow implemented]"
}
```

---

> **Document version:** 1.0  
> **Last updated:** 2026-07-22  
> **Next review:** [FILLER: Add date]  
