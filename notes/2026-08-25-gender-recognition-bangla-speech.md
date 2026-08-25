---
title: "Benchmarking Machine Learning and Deep Learning Models for Gender Recognition from Bangla Speech"
authors: "Mainul Islam, Irtiza Hasan, Mohammad Ehsanul Hoque, Salman Jubair Jim†, Md Nabi Newaz Khan, Md. Nawab Yousuf Ali"
venue: "IEEE ICCIT"
year: 2025
url: "https://ieeexplore.ieee.org/document/11491644#page=0.92"
area: "ml"
depth: skim
date_read: "2026-08-25"
---

<!--
area:      ml | nlp | security
depth:     deep | skim
date_read: YYYY-MM-DD
Save as notes/YYYY-MM-DD-short-slug.md, then run: python scripts/update_index.py
-->

## What problem

<!-- The question the paper is actually trying to answer, in my own words. -->
The acoustic characteristics of speech are influenced by various factors, including the speaker’s identity, gender, emotional state, and age. Bengali is one of the most widely spoken languages in the world. Yet, it lacks speech based gender recognition. This paper tries to answer this by employing some ML and DL models. 

## Prior work and its gap

<!-- What people did before, and the specific thing it couldn't do. -->
Uddin et al. applied SVM and KNN with MFCC features across three datasets, finding that KNN outperformed SVM. But they did not apply any neural network based model. Hamdi et. al used Arabic Natural Audio Dataset (ANAD) with ML models including SVM, CatBoost, XGBoost and RF alongwith simple ANN model. They lacked more capable NN based approach including LSTM and BiLSTM. Which was applied on both Arabic and English languages by Mohammed and Al-Irhayim. Despite such advances, the gap remained Bengali specific. 


## Method in 3 sentences

<!-- No more than three. If it takes more, I haven't understood it yet. -->
The overall workflow is as follows: (1) audio input acquisition, (2) MFCC feature extraction, (3) feature standardization, (4) 80/20 train-test split, (5) model training (SVM, KNN, LSTM, or stacking ensemble), and (6) gender classification output.

## Data and metrics

<!-- Datasets, splits, and what is being measured. -->
Three datasets were used throughout this evaluation. They are: (1) KUET Bangla Emotional Speech (KBES), (2) Bangla Emotional Speech Recognition Dataset (BANSpEmo), and (3) Bangla Speech Emotion Recognition
(BanglaSER).

## Headline result

<!-- The one number worth remembering, with what it's compared against. -->
Experimental results show that LSTM consistently achieves the highest accuracy across datasets (93.889% on KBES, 99.371% on BANSpEmo, and 94.558% on BanglaSER), while the ensemble method outperforms individual ML classifiers. So, LSTM > Ensemble (SVM + KNN) > Individual ML Model

## What I learned that I didn't know

<!-- The part that changed my mental model, not a summary of the abstract. -->
I learned the term Mel Frequency Cepstral Coefficients (MFCC) for feature extraction. It captures the spectral properties that reflects differences in vocal tract structure between males and females.

## What I'm unsure about

<!-- Claims I can't evaluate, experiments I'd want, things that smell off. -->
I can't evaluate their claimed results. It is impossible without rebuilding their exact experimental setup. I think their contribution is too much narrow. Because they didnot construct any dataset or propose any new model with custom settings rather they used 3 datasets on Bengali language.  

## Terms I had to look up

<!-- Vocabulary, with short definitions, so the next paper is cheaper. -->

- **Mel Frequency Cepstral Coefficients (MFCC)** — Mel-frequency cepstral coefficients (MFCCs) are a small set of features that concisely describe the overall shape of a sound's power spectrum, mimicking how the human ear perceives pitch and loudness.
- **Optimal Hyperplane** - An optimal hyperplane is the decision boundary in a Support Vector Machine (SVM) that separates data classes while maximizing the distance (margin) to the nearest points of each class
- **Librosa Python Library** - Librosa is a popular open-source Python library used for audio and music signal processing. It provides the foundational building blocks to create Music Information Retrieval (MIR) systems, analyze speech, and extract acoustic features for machine learning models.

## Future Scopes

<!-- Any future directions possible from the paper -->
+ Producing more larger and diverse Bengali speech dataset 
+ Exploring additional models like RF, BiLSTM, CNN etc.
