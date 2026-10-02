import streamlit as st, pandas as pd, plotly.graph_objects as go
from utils import setup, hero, load_data, load_artifacts, FEATURES, LABELS, CROPS

setup("Crop Recommender", "🌱")
hero("Crop Recommender 🌱", "Tell us about your land and climate.", "paddy_field.jpg")
df = load_data(); model, scaler, le, _ = load_artifacts()
RANGES = {"Nitrogen": (0, 140, 50), "Phosphorous": (5, 145, 53), "Potassium": (5, 205, 48), "temperature": (8.0, 44.0, 25.0),
          "humidity": (14.0, 100.0, 71.0), "ph": (3.5, 10.0, 6.5), "rainfall": (20.0, 300.0, 100.0)}

def preset(crop):
    for f, v in df[df.crop == crop][FEATURES].mean().items():
        lo, hi, _ = RANGES[f]; st.session_state[f] = type(lo)(round(min(max(v, lo), hi), 1))
for f, (lo, hi, d) in RANGES.items(): st.session_state.setdefault(f, d)

st.selectbox("Quick start: load typical values for a crop (optional)", [""] + sorted(df.crop.unique()),
             key="preset", on_change=lambda: st.session_state.preset and preset(st.session_state.preset))
l, r = st.columns(2)
with l:
    st.markdown("#### 🧪 Soil nutrients")
    vals = {f: st.slider(LABELS[f], *RANGES[f][:2], key=f) for f in FEATURES[:3] + ["ph"]}
with r:
    st.markdown("#### 🌦️ Weather")
    vals.update({f: st.slider(LABELS[f], *RANGES[f][:2], key=f) for f in ["temperature", "humidity", "rainfall"]})

if st.button("🌾 Recommend the best crop"):
    x = scaler.transform(pd.DataFrame([[vals[f] for f in FEATURES]], columns=FEATURES))
    proba = model.predict_proba(x)[0]; top = proba.argsort()[::-1][:5]
    best = le.classes_[top[0]]; emoji, season, tip = CROPS.get(best, ("🌱", "-", ""))
    a, b = st.columns([1, 1.3])
    with a:
        st.markdown(f'<div class="result"><div class="big">{emoji}</div><h2>{best}</h2>'
                    f'<p><b>{proba[top[0]]*100:.1f}% confidence</b></p><p>🗓️ {season}</p><p>💡 {tip}</p></div>',
                    unsafe_allow_html=True)
    with b:
        fig = go.Figure(go.Bar(x=[proba[i]*100 for i in top][::-1], y=[le.classes_[i].title() for i in top][::-1],
                               orientation="h", marker_color=["#C6A700", "#A5D6A7", "#66BB6A", "#43A047", "#2E7D32"]))
        fig.update_layout(title="Top 5 matching crops (%)", height=330, margin=dict(l=10, r=10, t=50, b=10),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig)
    ideal = df[df.crop == best][FEATURES].mean()
    cmp = pd.DataFrame({"Your input": [vals[f] for f in FEATURES], f"Typical for {best}": ideal.round(1).values},
                       index=[LABELS[f] for f in FEATURES])
    st.markdown("#### Your conditions vs. what this crop usually gets")
    st.dataframe(cmp)
