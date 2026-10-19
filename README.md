# Credit Card Fraud Detection (ML Project) – Step-by-Step Guide

Is document me project ko **chhote se chhote steps** me likha gaya hai. Bas upar se neeche ek-ek step follow karo.

**Goal:** Ek Machine Learning model banana jo bataye ki koi credit card transaction **Fraud (1)** hai ya **Normal (0)**.

---

## Phase 0 – Setup (Computer taiyar karo)

1. Python install karo (version 3.9 ya usse naya) – https://www.python.org/downloads/
2. Install karte waqt **"Add Python to PATH"** wala box tick karo.
3. Terminal / Command Prompt kholo aur check karo:
   ```bash
   python --version
   ```
4. Git install karo – https://git-scm.com/downloads
5. Check karo:
   ```bash
   git --version
   ```
6. VS Code install karo (code likhne ke liye) – https://code.visualstudio.com/
7. VS Code me **Python** aur **Jupyter** extension install karo.

## Phase 1 – Repo ko apne computer par laao

8. Terminal me wo folder kholo jaha project rakhna hai.
9. Repo clone karo:
   ```bash
   git clone https://github.com/RIAURAI/nisansya-ml-Credit-Card-Fraud-Detection.git
   ```
10. Folder ke andar jao:
    ```bash
    cd nisansya-ml-Credit-Card-Fraud-Detection
    ```
11. Ye folders banao:
    ```bash
    mkdir data notebooks src models
    ```
    - `data/` → dataset
    - `notebooks/` → Jupyter notebooks
    - `src/` → Python scripts
    - `models/` → trained model files

## Phase 2 – Virtual Environment banao

12. Virtual environment banao:
    ```bash
    python -m venv venv
    ```
13. Use activate karo:
    - Windows: `venv\Scripts\activate`
    - Mac/Linux: `source venv/bin/activate`
14. Terminal me `(venv)` dikhna chahiye – matlab sahi hai.
15. `requirements.txt` naam ki file banao aur isme ye likho:
    ```
    pandas
    numpy
    matplotlib
    seaborn
    scikit-learn
    imbalanced-learn
    xgboost
    joblib
    jupyter
    streamlit
    ```
16. Sab libraries install karo:
    ```bash
    pip install -r requirements.txt
    ```

## Phase 3 – Dataset download karo

17. Kaggle par account banao – https://www.kaggle.com/
18. Dataset kholo: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
19. **Download** button dabao (zip file aayegi).
20. Zip ko extract karo → `creditcard.csv` milegi.
21. `creditcard.csv` ko `data/` folder me rakho.
22. `.gitignore` file banao aur isme likho (badi file GitHub par nahi jaani chahiye):
    ```
    venv/
    data/*.csv
    __pycache__/
    .ipynb_checkpoints/
    ```

> **Dataset ke baare me:** 2,84,807 transactions hain, jisme sirf 492 fraud hain (~0.17%). Columns: `Time`, `V1`–`V28` (hidden/PCA features), `Amount`, aur `Class` (0 = Normal, 1 = Fraud).

## Phase 4 – Notebook shuru karo

23. Terminal me likho:
    ```bash
    jupyter notebook
    ```
24. Browser khulega → `notebooks/` folder me jao.
25. **New → Python 3** se naya notebook banao, naam rakho `fraud_detection.ipynb`.

## Phase 5 – Data load karo

26. Pehle cell me libraries import karo:
    ```python
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    ```
27. Data load karo:
    ```python
    df = pd.read_csv('../data/creditcard.csv')
    ```
28. Pehli 5 rows dekho: `df.head()`
29. Rows aur columns ki ginti dekho: `df.shape`
30. Column info dekho: `df.info()`

## Phase 6 – Data samjho (EDA)

31. Missing values check karo: `df.isnull().sum()` (sab 0 hone chahiye).
32. Duplicate rows check karo: `df.duplicated().sum()`
33. Duplicates hatao: `df = df.drop_duplicates()`
34. Fraud vs Normal count dekho: `df['Class'].value_counts()`
35. Iska bar chart banao:
    ```python
    sns.countplot(x='Class', data=df)
    plt.show()
    ```
36. Note karo: data **bahut imbalanced** hai (fraud bahut kam hai). Ye baad me handle karna hai.
37. `Amount` ka distribution dekho:
    ```python
    sns.histplot(df['Amount'], bins=50)
    plt.show()
    ```
38. Fraud aur Normal ka average amount compare karo:
    ```python
    df.groupby('Class')['Amount'].mean()
    ```
39. Correlation heatmap banao:
    ```python
    plt.figure(figsize=(12,10))
    sns.heatmap(df.corr(), cmap='coolwarm')
    plt.show()
    ```

## Phase 7 – Data taiyar karo (Preprocessing)

40. `Amount` aur `Time` ko scale karo (baaki V1–V28 pehle se scaled hain):
    ```python
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df[['Amount', 'Time']] = scaler.fit_transform(df[['Amount', 'Time']])
    ```
41. Features (X) aur target (y) alag karo:
    ```python
    X = df.drop('Class', axis=1)
    y = df['Class']
    ```
42. Train aur Test data me baanto (80% / 20%):
    ```python
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    ```
    > `stratify=y` zaroori hai taaki dono me fraud ka ratio same rahe.

## Phase 8 – Imbalance handle karo

43. SMOTE import karo:
    ```python
    from imblearn.over_sampling import SMOTE
    ```
44. **Sirf training data** par SMOTE lagao (test data ko kabhi mat chhuo):
    ```python
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)
    ```
45. Check karo ab dono class barabar hain: `y_train_res.value_counts()`

## Phase 9 – Model banao

46. **Model 1 – Logistic Regression** (simple baseline):
    ```python
    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train_res, y_train_res)
    ```
47. **Model 2 – Random Forest:**
    ```python
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train_res, y_train_res)
    ```
48. **Model 3 – XGBoost:**
    ```python
    from xgboost import XGBClassifier
    xgb = XGBClassifier(random_state=42, eval_metric='logloss')
    xgb.fit(X_train_res, y_train_res)
    ```

## Phase 10 – Model check karo (Evaluation)

49. Evaluation tools import karo:
    ```python
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score
    ```
50. Har model ke liye ye chalao (example Random Forest ka):
    ```python
    y_pred = rf.predict(X_test)
    y_prob = rf.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print('ROC-AUC:', roc_auc_score(y_test, y_prob))
    print('PR-AUC:', average_precision_score(y_test, y_prob))
    ```
51. **Accuracy par bharosa mat karo** – sab ko "Normal" bolke bhi 99.8% accuracy aa jaati hai.
52. In cheezon ko dekho:
    - **Recall (Fraud)** → kitne fraud pakde (jitna zyada utna achha)
    - **Precision (Fraud)** → jo fraud bola, usme kitne sach me fraud the
    - **F1-score** aur **PR-AUC**
53. Teeno models ke results ek table me likho aur compare karo.
54. Sabse achha model choose karo (usually XGBoost ya Random Forest).

## Phase 11 – Model ko behtar karo (Optional)

55. Threshold badal ke dekho (0.5 ki jagah 0.3, 0.4 etc.):
    ```python
    y_pred_new = (y_prob > 0.3).astype(int)
    ```
56. `GridSearchCV` ya `RandomizedSearchCV` se best parameters dhoondo.
57. Feature importance dekho:
    ```python
    pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False).head(10)
    ```

## Phase 12 – Model save karo

58. Best model aur scaler save karo:
    ```python
    import joblib
    joblib.dump(rf, '../models/fraud_model.pkl')
    joblib.dump(scaler, '../models/scaler.pkl')
    ```
59. Check karo ki `models/` folder me dono files aa gayi.

## Phase 13 – Simple App banao (Optional)

60. `src/app.py` file banao.
61. Isme Streamlit use karke model load karo aur user se CSV upload karwao.
62. Upload hui transactions par prediction dikhao (Fraud / Normal).
63. App chalao:
    ```bash
    streamlit run src/app.py
    ```

## Phase 14 – GitHub par code daalo

64. Status dekho: `git status`
65. Sab files add karo: `git add .`
66. Commit karo: `git commit -m "Added fraud detection notebook and model"`
67. Push karo: `git push origin main`
68. GitHub par repo kholke check karo ki files aa gayi.

## Phase 15 – Final kaam

69. Is README me **Results** section add karo (best model ka Recall, Precision, F1, ROC-AUC).
70. Confusion matrix aur charts ke screenshots add karo.
71. **"How to run"** section likho (Phase 2, 3, 4 ke commands).
72. Final commit aur push karo. ✅ Project complete!

---

## Final Folder Structure

```
nisansya-ml-Credit-Card-Fraud-Detection/
├── data/                  # creditcard.csv (GitHub par upload nahi hoga)
├── notebooks/
│   └── fraud_detection.ipynb
├── src/
│   └── app.py
├── models/
│   ├── fraud_model.pkl
│   └── scaler.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

## Quick Checklist

- [ ] Setup done (Python, Git, VS Code)
- [ ] Repo clone + folders bane
- [ ] venv + libraries install
- [ ] Dataset download
- [ ] EDA done
- [ ] Preprocessing + Train/Test split
- [ ] SMOTE applied
- [ ] 3 models trained
- [ ] Evaluation + comparison
- [ ] Model saved
- [ ] App (optional)
- [ ] Code pushed to GitHub
- [ ] README me results add
