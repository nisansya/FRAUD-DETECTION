# 💳 Credit Card Fraud Detection

An end-to-end Machine Learning project that detects fraudulent credit card transactions in real-time using a Streamlit web app.

Built with Python, Scikit-Learn, XGBoost, and deployed with **Docker & Streamlit**.

**Trained on 284,807 real-world transactions.**

---

## 🚀 Live Demo

**Try the App:** [Click here to open the Live App](https://your-streamlit-link-here.streamlit.app](https://fraud-detection-vjmbevyratpgvf3tdvmndc.streamlit.app/)

**Docker Hub:** [nisansya/fraud-app:1.0](https://hub.docker.com/r/nisansya/fraud-app](https://hub.docker.com/repository/docker/nisansya/fraud-app/general)

---

## ✨ Features

- **Real-time Prediction:** Upload a CSV file and get fraud predictions instantly
- **Single Transaction Check:** Manually enter transaction details to check if it's fraud
- **Transaction Analysis:** Visualize fraud vs normal transactions with interactive charts
- **Batch Processing:** Predict on thousands of transactions at once
- **Download Results:** Export predictions as a CSV file
- **High Accuracy:** Handles highly imbalanced data using SMOTE

---

## 🛠️ Tech Stack

- **Language:** Python 3.13
- **Web App:** Streamlit
- **ML Libraries:** Scikit-Learn, XGBoost, Imbalanced-Learn (SMOTE)
- **Data:** Pandas, NumPy, Plotly
- **Deployment:** Docker, Docker Hub, Streamlit Cloud
- **Models Used:** Random Forest, XGBoost

---

## 📁 Project Structure
    ```
    nisansya-ml-Credit-Card-Fraud-Detection/
    - `data/` → dataset
    - `notebooks/` → Jupyter notebooks
    - `src/` → Python scripts
    - `models/` → trained model files
    - `requirements.txt` # App dependencies
    -`Dockerfile` # Docker setup
    -`.dockerignore ` # Files to ignore in


---

## 📊 Dataset

- **Source:** [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Total Transactions:** 284,807
- **Fraud Transactions:** 492 (0.172% - Highly Imbalanced)
- **Features:** `Time`, `Amount`, `V1` to `V28` (PCA transformed), `Class` (0 = Normal, 1 = Fraud)

---

## 📈 Model Performance

| Model | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: |
| Random Forest | 0.89 | 0.77 | 0.82 | 0.96 |
| **XGBoost (Best)** | **0.83** | **0.80** | **0.81** | **0.95** |

---

## ⚙️ How to Run Locally

### 1. Clone the Repo
```bash
git clone https://github.com/nisansya/FRAUD-DETECTION.git
cd FRAUD-DETECTION
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt4.
```

### 4. Run the App
```bash
streamlit run app.py
```

### 🐳 Run with Docker (Recommended)
You don't need Python or any setup. Just Docker.
Option 1: Pull from Docker Hub
```bash
docker pull nisansya/fraud-app:1.0
docker run -p 8501:8501 nisansya/fraud-app:1.0
```

Option 2: Build Locally
```bash
docker build -t fraud-app:1.0 .
docker run -p 8501:8501 fraud-app:1.0
```
Now open http://localhost:8501 in your browser.

## How It Works
### 1. Data Cleaning: Checked for missing values & duplicates.
### 2. EDA: Found data is highly imbalanced (only 0.17% fraud).
### 3. Preprocessing: Scaled Amount and Time using StandardScaler.
### 4. Handling Imbalance: Used SMOTE to balance fraud and normal classes in training data.
### 5. Training: Trained Random Forest, and XGBoost.
### 6. Evaluation: Compared models using Precision, Recall, and ROC-AUC (Accuracy alone is misleading here).
### 7. Deployment: Saved best model as .pkl and deployed with Streamlit + Docker.    
