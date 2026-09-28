# Task 6: RAG Answer Quality Evaluation Report

Evaluation conducted on exactly **10 test questions** grounded in the Mars exploration dataset.

## Evaluation Metrics
1. **Retrieval Score (1-5)**: Measures whether the retrieved chunks contain the required facts.
2. **Faithfulness Score (1-5)**: Measures whether the generated answer is accurate and supported by the context without hallucination.

### Summary: Average Retrieval: 4.70/5.0 | Average Faithfulness: 4.40/5.0

## Detailed Evaluation Records

### Question 1: Where did the Curiosity rover land, and on what date?

- **Expected Facts**: Gale Crater, August 6, 2012.
- **Generated Answer**: According to the provided context, the Curiosity rover landed inside Gale Crater on Mars on August 6, 2012.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: Launched in November 2011 and landing inside Gale Crater on Mars on August 6, 2012, Curiosity is a car-sized rover weighing approximately 899 kilograms. Curiosity was designed to assess whether Mars ever had an environment capable of supporting microbial life
>
> **Chunk 2**: ## The Curiosity Rover (Mars Science Laboratory)
>

---

### Question 2: What kind of power source does Curiosity use, and how many watts does it generate?

- **Expected Facts**: Multi-Mission Radioisotope Thermoelectric Generator (MMRTG), 110 watts.
- **Generated Answer**: According to the provided context, Curiosity uses a Multi-Mission Radioisotope Thermoelectric Generator (MMRTG) as its power source, which generates 110 watts of electrical power.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: . The MMRTG produces 110 watts of electrical power using heat from decaying plutonium-238, allowing Curiosity to operate through severe Martian dust storms and cold winter nights without power loss. Curiosity's scientific payload includes:
>
> **Chunk 2**: Unlike previous Mars rovers that relied exclusively on solar panels, Curiosity is powered by a Multi-Mission Radioisotope Thermoelectric Generator (MMRTG)
>

---

### Question 3: What was the purpose of the MOXIE instrument on Perseverance, and how much oxygen did it produce?

- **Expected Facts**: Extract breathable oxygen from Martian CO2; produced over 120 grams.
- **Generated Answer**: According to the provided context, the purpose of the MOXIE instrument on Perseverance was to demonstrate extracting breathable oxygen (O2) from the carbon dioxide (CO2) rich Martian atmosphere. Additionally, MOXIE produced over 120 grams of oxygen during its operational test phase.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: 4. MOXIE (Mars Oxygen ISRU Experiment): Technology demonstration that demonstrated extracting breathable oxygen (O2) from the carbon dioxide (CO2) rich Martian atmosphere. MOXIE produced over 120 grams of oxygen during its operational test phase.
>
> **Chunk 2**: ### Perseverance Core Objectives and Instruments Perseverance focuses on astrobiology and caching geological core samples for a future Mars Sample Return mission. Key instruments on Perseverance include:
>

---

### Question 4: Why was Jezero Crater chosen as the landing site for Perseverance?

- **Expected Facts**: Contains ancient river delta into paleolake; ideal for preserving biosignatures.
- **Generated Answer**: According to the provided context, Jezero Crater was chosen as the landing site for Perseverance because it contains an ancient river delta that fed into a paleolake billions of years ago, making it an ideal location to preserve biosignatures.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: The Perseverance rover landed in Jezero Crater on February 18, 2021. Jezero Crater was selected because it contains an ancient river delta that fed into a paleolake billions of years ago, making it an ideal location to preserve biosignatures
>
> **Chunk 2**: . Perseverance weighs roughly 1,025 kilograms and is built on a modified Curiosity chassis, featuring an upgraded autonomous navigation system called AutoNav that enables it to traverse Martian terrain five times faster than Curiosity.
>

---

### Question 5: How much does the Ingenuity helicopter weigh, and how fast do its blades spin?

- **Expected Facts**: 1.8 kilograms; 2,400 to 2,700 RPM.
- **Generated Answer**: According to the provided context, Ingenuity weighs 1.8 kilograms. Additionally, its carbon-fiber rotor blades spin at approximately 2,400 to 2,700 revolutions per minute (RPM), which is nearly five times faster than standard terrestrial helicopter blades.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: . To generate sufficient aerodynamic lift in such thin air, Ingenuity utilized counter-rotating carbon-fiber rotor blades spinning at approximately 2,400 to 2,700 revolutions per minute (RPM)—nearly five times faster than standard terrestrial helicopter blades
>
> **Chunk 2**: Ingenuity is an ultra-lightweight autonomous drone helicopter that accompanied Perseverance to Mars as a technology demonstration. Weighing only 1.8 kilograms, Ingenuity achieved the first powered, controlled flight on another planet on April 19, 2021. The Martian atmosphere has an atmospheric density less than 1 percent of Earth's at sea level
>

---

### Question 6: How many flights did Ingenuity complete compared to its original mission plan?

- **Expected Facts**: 72 flights completed vs 5 originally planned.
- **Generated Answer**: According to the context, Ingenuity completed 72 flights over nearly three years, whereas its original mission plan was for only 5 test flights over 30 days. Therefore, the answer is:

Ingenuity completed 67 flights more than its original mission plan.
- **Retrieval Relevance Score**: 4/5 — *Retrieved chunks contain the main facts with minor gaps.*
- **Answer Faithfulness Score**: 4/5 — *Answer is mostly accurate and supported.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: . Although originally designed for only five test flights over 30 days, Ingenuity completed 72 flights over nearly three years, serving as an aerial scout for Perseverance.
>
> **Chunk 2**: Ingenuity is an ultra-lightweight autonomous drone helicopter that accompanied Perseverance to Mars as a technology demonstration. Weighing only 1.8 kilograms, Ingenuity achieved the first powered, controlled flight on another planet on April 19, 2021. The Martian atmosphere has an atmospheric density less than 1 percent of Earth's at sea level
>

---

### Question 7: What is the atmospheric pressure on Mars, and what is its primary chemical composition?

- **Expected Facts**: Approx. 6 millibars (less than 1% of Earth); 95% carbon dioxide.
- **Generated Answer**: According to the provided documents, the atmospheric pressure on Mars is approximately 6 millibars, and its primary chemical composition is 95% carbon dioxide, 2.6% nitrogen, and 1.9% argon.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 4/5 — *Answer is mostly accurate and supported.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: ## Environmental Challenges on the Martian Surface Exploration rovers face severe environmental challenges on Mars: 1. Atmospheric Pressure and Composition: Atmospheric pressure is approximately 6 millibars (less than 1% of Earth's), composed of 95% carbon dioxide, 2.6% nitrogen, and 1.9% argon.
>
> **Chunk 2**: 4. MOXIE (Mars Oxygen ISRU Experiment): Technology demonstration that demonstrated extracting breathable oxygen (O2) from the carbon dioxide (CO2) rich Martian atmosphere. MOXIE produced over 120 grams of oxygen during its operational test phase.
>

---

### Question 8: What causes radio communication delays between Earth and Mars, and how long are they?

- **Expected Facts**: Distance between planets; radio signals take between 3 and 22 minutes each way.
- **Generated Answer**: According to the provided context, the distance between Earth and Mars causes radio communication delays, which take between 3 and 22 minutes each way.
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 5/5 — *Answer accurately states facts directly supported by the context.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: . Due to the distance between Earth and Mars, radio signals take between 3 and 22 minutes each way, necessitating autonomous navigation and operation systems for surface vehicles.
>
> **Chunk 2**: 3. Dust Storms: Local and global dust storms can blanket the sky for months, drastically attenuating sunlight, which previously ended the solar-powered Opportunity rover mission in 2018.
>

---

### Question 9: What is the function of the ChemCam instrument on Curiosity?

- **Expected Facts**: Laser-induced breakdown spectrometer vaporizing rock up to 7m away for elemental composition.
- **Generated Answer**: According to the provided documents, the function of the ChemCam instrument on Curiosity is to "vaporize rock surfaces up to 7 meters away to determine elemental composition."
- **Retrieval Relevance Score**: 5/5 — *Retrieved chunks contain all necessary factual details.*
- **Answer Faithfulness Score**: 4/5 — *Answer is mostly accurate and supported.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: 1. Mastcam: Color stereoscopic imaging system mounted on the rover mast. 2. ChemCam: Laser-induced breakdown spectrometer that vaporizes rock surfaces up to 7 meters away to determine elemental composition. 3. SAM (Sample Analysis at Mars): Suite of instruments including a gas chromatograph and mass spectrometer to search for organic molecules.
>
> **Chunk 2**: 1. SuperCam: Upgraded successor to ChemCam that provides laser spectroscopy, infrared imaging, and an acoustic microphone to record Martian wind sounds. 2. PIXL (Planetary Instrument for X-ray Lithochemistry): Micro-focus X-ray fluorescence spectrometer that maps rock elemental chemistry at sub-millimeter scales.
>

---

### Question 10: Why did the solar-powered Opportunity rover mission end in 2018?

- **Expected Facts**: Severe Martian dust storm that blanketed the sky for months and blocked sunlight.
- **Generated Answer**: According to the provided context, the solar-powered Opportunity rover mission ended in 2018 because "drastically attenuating sunlight" caused by a dust storm.
- **Retrieval Relevance Score**: 3/5 — *Retrieved chunks partially address the question.*
- **Answer Faithfulness Score**: 2/5 — *Answer lacks key factual verification.*

**Retrieved Chunks Used as Context**:
> **Chunk 1**: 3. Dust Storms: Local and global dust storms can blanket the sky for months, drastically attenuating sunlight, which previously ended the solar-powered Opportunity rover mission in 2018.
>
> **Chunk 2**: # Mars Robotic Exploration and Rover Systems
>

---

