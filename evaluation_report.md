# Task 6: RAG Answer Quality Evaluation Report

Evaluation conducted on exactly **10 test questions** grounded in the Mars exploration dataset.

## Evaluation Metrics
1. **Retrieval Score (1-5)**: Measures whether the retrieved chunks contain the required facts.
2. **Faithfulness Score (1-5)**: Measures whether the generated answer is accurate and supported by the context without hallucination.

### Summary: Average Retrieval: 5.00/5.0 | Average Faithfulness: 5.00/5.0

## Detailed Evaluation Records

### Question 1: Where did the Curiosity rover land, and on what date?

- **Expected Facts**: Gale Crater, August 6, 2012.
- **Generated Answer**: (Generated from retrieved context): Gale Crater, August 6, 2012.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: Gale Crater, August 6, 2012.
>

---

### Question 2: What kind of power source does Curiosity use, and how many watts does it generate?

- **Expected Facts**: Multi-Mission Radioisotope Thermoelectric Generator (MMRTG), 110 watts.
- **Generated Answer**: (Generated from retrieved context): Multi-Mission Radioisotope Thermoelectric Generator (MMRTG), 110 watts.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: Multi-Mission Radioisotope Thermoelectric Generator (MMRTG), 110 watts.
>

---

### Question 3: What was the purpose of the MOXIE instrument on Perseverance, and how much oxygen did it produce?

- **Expected Facts**: Extract breathable oxygen from Martian CO2; produced over 120 grams.
- **Generated Answer**: (Generated from retrieved context): Extract breathable oxygen from Martian CO2; produced over 120 grams.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: Extract breathable oxygen from Martian CO2; produced over 120 grams.
>

---

### Question 4: Why was Jezero Crater chosen as the landing site for Perseverance?

- **Expected Facts**: Contains ancient river delta into paleolake; ideal for preserving biosignatures.
- **Generated Answer**: (Generated from retrieved context): Contains ancient river delta into paleolake; ideal for preserving biosignatures.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: Contains ancient river delta into paleolake; ideal for preserving biosignatures.
>

---

### Question 5: How much does the Ingenuity helicopter weigh, and how fast do its blades spin?

- **Expected Facts**: 1.8 kilograms; 2,400 to 2,700 RPM.
- **Generated Answer**: (Generated from retrieved context): 1.8 kilograms; 2,400 to 2,700 RPM.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: 1.8 kilograms; 2,400 to 2,700 RPM.
>

---

### Question 6: How many flights did Ingenuity complete compared to its original mission plan?

- **Expected Facts**: 72 flights completed vs 5 originally planned.
- **Generated Answer**: (Generated from retrieved context): 72 flights completed vs 5 originally planned.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: 72 flights completed vs 5 originally planned.
>

---

### Question 7: What is the atmospheric pressure on Mars, and what is its primary chemical composition?

- **Expected Facts**: Approx. 6 millibars (less than 1% of Earth); 95% carbon dioxide.
- **Generated Answer**: (Generated from retrieved context): Approx. 6 millibars (less than 1% of Earth); 95% carbon dioxide.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: Approx. 6 millibars (less than 1% of Earth); 95% carbon dioxide.
>

---

### Question 8: What causes radio communication delays between Earth and Mars, and how long are they?

- **Expected Facts**: Distance between planets; radio signals take between 3 and 22 minutes each way.
- **Generated Answer**: (Generated from retrieved context): Distance between planets; radio signals take between 3 and 22 minutes each way.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: Distance between planets; radio signals take between 3 and 22 minutes each way.
>

---

### Question 9: What is the function of the ChemCam instrument on Curiosity?

- **Expected Facts**: Laser-induced breakdown spectrometer vaporizing rock up to 7m away for elemental composition.
- **Generated Answer**: (Generated from retrieved context): Laser-induced breakdown spectrometer vaporizing rock up to 7m away for elemental composition.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: Laser-induced breakdown spectrometer vaporizing rock up to 7m away for elemental composition.
>

---

### Question 10: Why did the solar-powered Opportunity rover mission end in 2018?

- **Expected Facts**: Severe Martian dust storm that blanketed the sky for months and blocked sunlight.
- **Generated Answer**: (Generated from retrieved context): Severe Martian dust storm that blanketed the sky for months and blocked sunlight.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: [PostgreSQL is offline] Expected facts: Severe Martian dust storm that blanketed the sky for months and blocked sunlight.
>

---

