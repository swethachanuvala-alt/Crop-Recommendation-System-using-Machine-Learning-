import streamlit as st
from utils import setup, hero, load_data, CROPS, FEATURES

setup("Crop Guide", "📖")
hero("Crop Guide 📖", "Season, climate and soil tips for all 22 crops.", "harvest_basket.jpg")
df = load_data(); q = st.text_input("🔍 Search a crop").lower()
means = df.groupby("crop")[FEATURES].mean().round(0)
names = [c for c in sorted(CROPS) if q in c]
for i in range(0, len(names), 3):
    for col, c in zip(st.columns(3), names[i:i+3]):
        e, season, tip = CROPS[c]; r = means.loc[c]
        col.markdown(f'<div class="card"><div style="font-size:2.4rem">{e}</div><h4>{c.title()}</h4>'
                     f'<small>🗓️ {season}</small><p>{tip}</p><small>N {r.Nitrogen:.0f} · P {r.Phosphorous:.0f} · K {r.Potassium:.0f}<br>'
                     f'{r.temperature:.0f}°C · {r.humidity:.0f}% humidity · {r.rainfall:.0f} mm rain</small></div><br>', unsafe_allow_html=True)
