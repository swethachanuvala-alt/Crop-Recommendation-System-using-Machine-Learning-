import streamlit as st, plotly.express as px
from utils import setup, hero, load_artifacts, LABELS

setup("Model Insights", "🧠")
hero("Model Insights 🧠", "How well does our XGBoost model understand your farm?", "tractor_field.jpg")
_, _, le, m = load_artifacts()
c = st.columns(4)
for col, (k, n) in zip(c, [("accuracy", "Accuracy"), ("precision", "Precision"), ("recall", "Recall"), ("f1", "F1 score")]):
    col.metric(n, f"{m[k]*100:.2f}%")
st.caption(f"Trained on {m['n_train']} samples, tested on {m['n_test']} unseen samples. Scores are weighted averages.")
a, b = st.columns(2)
with a:
    imp = sorted(m["importance"].items(), key=lambda kv: kv[1])
    st.plotly_chart(px.bar(x=[v for _, v in imp], y=[LABELS[k] for k, _ in imp], orientation="h", title="What influences the prediction most",
                           color_discrete_sequence=["#2E7D32"], labels={"x": "Importance", "y": ""}))
with b:
    f1 = sorted(m["per_class_f1"].items(), key=lambda kv: kv[1])
    st.plotly_chart(px.bar(x=[v for _, v in f1], y=[k.title() for k, _ in f1], orientation="h", title="F1 score per crop",
                           color_discrete_sequence=["#F9A825"], labels={"x": "F1", "y": ""}))
st.plotly_chart(px.imshow(m["confusion"], x=m["classes"], y=m["classes"], color_continuous_scale="Greens",
                          title="Confusion matrix (test set)", labels=dict(x="Predicted", y="Actual"), height=700))
