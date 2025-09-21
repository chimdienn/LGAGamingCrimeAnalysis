# Victorian Vibes: EGMs Expenditure vs Drug-and-Alcohol-Related Crimes

This repository contains the code and report for **COMP20008 – Elements of Data Processing (Semester 2, 2024)** Assignment 2 at the University of Melbourne.  
Our group project investigates the relationship between **Electronic Gaming Machine (EGM) expenditure** and the **incidence of drug- and alcohol-related crimes** across Victorian Local Government Areas (LGAs) between 2014 and 2020.

---

## 📌 Research Question
> **What is the relationship between annual expenditure on EGMs and the annual prevalence of addictive substance use and disorderly alcohol-related crimes within each local government area between 2014 and 2020?**

---

## 📊 Project Overview
- **Datasets Used**:
  - `LGA_EGM.csv`: Annual gaming losses across 57 LGAs.
  - `LGA_Offences.xlsx`: Crime statistics (drug-related and alcohol-related offences).
- **Cleaning & Preprocessing**:
  - Harmonised LGAs across datasets (handling missing and merged LGAs).
  - Filtered offence subgroups into **drug-related** and **alcohol-related** categories.
  - Normalised data for clustering analysis.

- **Exploration**:
  - Line plots and heatmaps to examine temporal and regional trends.
  - Scatter plots to visualise cross-sectional relationships between gaming losses and offences.

- **Machine Learning Methods**:
  - **Linear Regression** (supervised): Modelled offence counts as a function of gaming losses, achieving an R² of ~0.704.
  - **K-Means Clustering** (unsupervised): Grouped LGAs into **high-loss/high-offence** vs **low-loss/low-offence** 

---

## 🔑 Key Findings
- LGAs with **higher gaming losses tend to report higher drug- and alcohol-related offences**.
- Stronger correlation between **EGM losses and drug-related offences** than alcohol-related offences.
- **No strong temporal relationship** — changes in gaming losses from year to year did not significantly influence offence counts.
- COVID-19 disruptions in 2020 caused a sharp decline in gaming losses across all LGAs.
- Clustering revealed distinct high-risk vs. low-risk groups of LGAs

---
📄 Deliverables

* Code: Python scripts implementing preprocessing, analysis, and models.
* Report: Detailed findings, methodology, and discussion of results.
* Slides & Presentation: Delivered in Week 12 (not included in repo).
