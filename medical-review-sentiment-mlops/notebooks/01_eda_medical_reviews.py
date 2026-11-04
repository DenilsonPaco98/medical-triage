"""Notebook 01 - EDA Medical Reviews.

Exploratory Data Analysis of medical reviews dataset.
"""

# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("../data/raw/medical_reviews.csv")

# Display basic info
print("Dataset shape:", df.shape)
print("\nFirst rows:")
print(df.head())

# Summary statistics
print("\nDataset info:")
print(df.info())

# Sentiment distribution
sentiment_counts = df["sentiment"].value_counts()
print("\nSentiment distribution:")
print(sentiment_counts)

# Text length analysis
df["text_length"] = df["text"].str.len()
print("\nText length statistics:")
print(df["text_length"].describe())
