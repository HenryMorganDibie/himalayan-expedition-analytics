# 🏔️ Himalayan Expedition Analytics Dashboard

An interactive data analytics dashboard built with **Streamlit**, **Altair**, and **Pandas**, exploring 100+ years of mountaineering history in the Nepalese Himalaya. This dataset, curated from the archives of Elizabeth Hawley, spans expeditions from **1905 to 2024**, including:

- 🧗‍♂️ 89,000+ climbers
- 🏕 11,000+ expeditions
- 🏔 480 mountain peaks (including Everest)
- 📜 Rich historical details like dates, successes, and significant events

---

## 📊 Key Features

- 🔍 Explore expedition data by **year** and **citizen country**
- 📌 Visualize **top 5 most climbed peaks**
- 🧠 Identify the **most successful climber** in history
- 📈 See trends in total vs. successful expeditions over time
- ⛰ Find out **how many people have summited Mount Everest**
- 📊 View dataset previews (Expeditions, Members, Peaks, References, Dictionary)
- 🧮 Instantly see the number of rows and columns per dataset

---

## 🧠 Dashboard Results

### ✅ 1. % of Peaks Climbed
> **86.67%** of all known Himalayan peaks have been climbed.

---

### ✅ 2. Most Successful Climber
> **Pasang** was the most frequently successful climber in the dataset.

---

### ✅ 3. Successful Everest Climbers
> A total of **12,712** people have successfully summited **Mount Everest**.

---

### ✅ 4. Dataset Dimensions

| Table        | Rows    | Columns |
|--------------|---------|---------|
| Expeditions  | 11,425  | 65      |
| Members      | 89,000  | 61      |
| Peaks        | 480     | 23      |
| References   | 15,586  | 12      |

---

### ✅ 5. Top 5 Most Climbed Peaks

Displayed in a bar chart — showing peak names and total number of climbers who attempted them. *(Use tooltip and dataframe to explore exact numbers.)*

---

## 🗂 Project Structure

henry-analytics-core/
├── himalayan-analytics/
│ ├── notepad.py # Streamlit dashboard app
│ └── datasets/ # Dataset folder
│ ├── exped.csv
│ ├── members.csv
│ ├── peaks.csv
│ ├── refer.csv
│ └── himalayan_data_dictionary.csv
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore rules
└── README.md # This file
