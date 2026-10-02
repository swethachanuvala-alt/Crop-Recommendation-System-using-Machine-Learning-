import streamlit as st
from utils import setup, hero, photo, load_data, load_artifacts

setup("Home")
hero("Grow the Right Crop, Every Season 🌾",
     "Enter your soil nutrients and weather conditions and our XGBoost model recommends the best crop for your farm.")
st.page_link("pages/1_Crop_Recommender.py", label="Get my crop recommendation →", icon="🌱")

df, (_, _, le, metrics) = load_data(), load_artifacts()
c = st.columns(4)
for col, (n, t) in zip(c, [(len(df), "Soil & weather records"), (len(le.classes_), "Crops supported"),
                           (7, "Input factors"), (f"{metrics['accuracy']*100:.1f}%", "Model accuracy")]):
    col.markdown(f'<div class="stat"><b>{n}</b><span>{t}</span></div>', unsafe_allow_html=True)

st.markdown("### How it works")
c = st.columns(3)
for col, (e, t, d) in zip(c, [("🧪", "1. Share your soil data", "Nitrogen, phosphorus, potassium and soil pH from a soil test."),
                              ("🌦️", "2. Add local weather", "Average temperature, humidity and rainfall for your area."),
                              ("🤖", "3. Get your crop", "XGBoost ranks the best crops with a confidence score and farming tips.")]):
    col.markdown(f'<div class="card"><div style="font-size:2.2rem">{e}</div><h4>{t}</h4>{d}</div>', unsafe_allow_html=True)

st.markdown("### Life on the farm")
c = st.columns(3)
with c[0]: photo("farmer_harvest.jpg", "Harvest season in the golden fields")
with c[1]: photo("paddy_field.jpg", "Tending the green paddy")
with c[2]: photo("tractor_field.jpg", "Preparing the soil for sowing")
st.caption("Illustrations are generated for this project. Replace the files in the assets/ folder with your own photos any time.")
