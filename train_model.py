"""Retrains the XGBoost crop model using the same pipeline as GGST_6.ipynb and saves everything in models/."""
import json, joblib, pandas as pd, numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
from xgboost import XGBClassifier

ROOT = Path(__file__).parent
FEATURES = ["Nitrogen", "Phosphorous", "Potassium", "temperature", "humidity", "ph", "rainfall"]

def train_and_save():
    df = pd.read_csv(ROOT / "data" / "Crop_recommendation.csv")
    df.columns = [str(c).strip() for c in df.columns]
    alias = {"label": "crop", "n": "Nitrogen", "p": "Phosphorous", "phosphorus": "Phosphorous", "k": "Potassium"}
    df = df.rename(columns={c: alias[c.lower()] for c in df.columns if c.lower() in alias}).dropna(how="all")
    for c in FEATURES: df[c] = df[c].fillna(df[c].median())
    df["crop"] = df["crop"].fillna(df["crop"].mode()[0])
    for c in FEATURES[1:]:                      # same IQR -> median outlier handling as the notebook
        q1, q3 = df[c].quantile(.25), df[c].quantile(.75); iqr = q3 - q1
        lo, hi, med = q1 - 1.5*iqr, q3 + 1.5*iqr, df[c].median()
        df[c] = df[c].apply(lambda x: med if x < lo or x > hi else x)
    le = LabelEncoder(); y = le.fit_transform(df["crop"]); X = df[FEATURES]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    scaler = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = scaler.transform(Xtr), scaler.transform(Xte)
    try:                                         # SMOTE is optional (the dataset is already balanced)
        from imblearn.over_sampling import SMOTE
        Xtr_s, ytr = SMOTE(random_state=42).fit_resample(Xtr_s, ytr)
    except Exception:
        pass
    model = XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42, eval_metric="mlogloss")
    model.fit(Xtr_s, ytr)
    pred = model.predict(Xte_s)
    p, r, f, _ = precision_recall_fscore_support(yte, pred, average="weighted", zero_division=0)
    metrics = {
        "accuracy": float(accuracy_score(yte, pred)), "precision": float(p), "recall": float(r), "f1": float(f),
        "train_accuracy": float(model.score(Xtr_s, ytr)), "n_train": int(len(Xtr)), "n_test": int(len(Xte)),
        "classes": list(le.classes_), "confusion": confusion_matrix(yte, pred).tolist(),
        "per_class_f1": {k: v["f1-score"] for k, v in classification_report(
            yte, pred, target_names=le.classes_, output_dict=True, zero_division=0).items() if k in le.classes_},
        "importance": dict(zip(FEATURES, map(float, model.feature_importances_))),
    }
    out = ROOT / "models"; out.mkdir(exist_ok=True)
    joblib.dump(model, out / "xg_boost_model.pkl"); joblib.dump(scaler, out / "scaler.pkl")
    joblib.dump({"crop": le}, out / "label_encoders.pkl")
    (out / "metrics.json").write_text(json.dumps(metrics))
    return metrics

if __name__ == "__main__":
    m = train_and_save()
    print(f"Done. Test accuracy: {m['accuracy']:.4f}  |  F1: {m['f1']:.4f}  -> files saved in models/")
