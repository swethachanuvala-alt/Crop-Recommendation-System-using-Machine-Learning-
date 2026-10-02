import base64, json, joblib, pandas as pd, streamlit as st
from pathlib import Path

ROOT = Path(__file__).parent
FEATURES = ["Nitrogen", "Phosphorous", "Potassium", "temperature", "humidity", "ph", "rainfall"]
LABELS = {"Nitrogen": "Nitrogen (N)", "Phosphorous": "Phosphorus (P)", "Potassium": "Potassium (K)",
          "temperature": "Temperature (°C)", "humidity": "Humidity (%)", "ph": "Soil pH", "rainfall": "Rainfall (mm)"}
GREENS = ["#1B5E20", "#2E7D32", "#66BB6A", "#C6A700", "#F9A825", "#8D6E63", "#A5D6A7"]

CROPS = {  # emoji, season, tip
 "rice": ("🌾", "Kharif (monsoon)", "Needs standing water and warm, humid weather; heavy rainfall suits it."),
 "maize": ("🌽", "Kharif / Rabi", "Well-drained loam and moderate rainfall; feed nitrogen in splits."),
 "chickpea": ("🫘", "Rabi (winter)", "Loves cool, dry weather; avoid waterlogging."),
 "kidneybeans": ("🫘", "Kharif", "Cool, moist climate and slightly acidic soil."),
 "pigeonpeas": ("🌱", "Kharif", "Drought tolerant; fixes nitrogen and enriches the soil."),
 "mothbeans": ("🌱", "Kharif", "Thrives in hot, dry, sandy soils with little rain."),
 "mungbean": ("🌱", "Kharif / Summer", "Short-duration pulse; warm weather and light rain."),
 "blackgram": ("🌱", "Kharif / Rabi", "Warm, humid climate; good for crop rotation."),
 "lentil": ("🫘", "Rabi", "Cool season crop that prefers low rainfall."),
 "pomegranate": ("🍎", "Perennial", "Hot, dry summers; deep watering but good drainage."),
 "banana": ("🍌", "Year-round", "High nitrogen and potassium; needs steady warmth and moisture."),
 "mango": ("🥭", "Perennial (summer fruit)", "Warm climate with a dry spell before flowering."),
 "grapes": ("🍇", "Perennial", "Very high phosphorus and potassium; needs sunshine and pruning."),
 "watermelon": ("🍉", "Summer", "Sandy loam, lots of sun and high potassium."),
 "muskmelon": ("🍈", "Summer", "Warm, dry weather and light irrigation for sweetness."),
 "apple": ("🍏", "Perennial (cool regions)", "Needs chilling winters and very high phosphorus and potassium."),
 "orange": ("🍊", "Perennial", "Humid subtropical climate with well-drained soil."),
 "papaya": ("🍈", "Year-round", "Hot, humid and frost-free; shallow roots hate waterlogging."),
 "coconut": ("🥥", "Perennial", "Coastal humid climate with high rainfall."),
 "cotton": ("☁️", "Kharif", "High nitrogen, warm weather and moderate rainfall."),
 "jute": ("🌿", "Kharif", "Hot, humid and high rainfall; thrives in alluvial soil."),
 "coffee": ("☕", "Perennial", "Shade-grown, warm humid highlands with rich nitrogen."),
}

def setup(title, icon="🌾"):
    st.set_page_config(page_title=f"{title} | Smart Crop Advisor", page_icon=icon, layout="wide")
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Merriweather:wght@700;900&display=swap');
    html, body, [class*="css"] {font-family:'Poppins',sans-serif;}
    h1,h2,h3 {font-family:'Merriweather',serif !important; color:#1B5E20;}
    #MainMenu, footer {visibility:hidden;}
    .block-container {padding-top:2rem; max-width:1200px;}
    [data-testid="stSidebar"] {background:linear-gradient(180deg,#2E7D32,#1B5E20);}
    [data-testid="stSidebar"] * {color:#F1F8E9 !important;}
    .hero {border-radius:22px; padding:80px 48px; color:#fff; background-size:cover; background-position:center;
           box-shadow:0 12px 30px rgba(27,94,32,.25); margin-bottom:1.5rem;}
    .hero h1 {color:#fff !important; font-size:3rem; text-shadow:0 2px 8px rgba(0,0,0,.4); margin:0;}
    .hero p {font-size:1.2rem; text-shadow:0 1px 6px rgba(0,0,0,.5); max-width:640px;}
    .card {background:#fff; border-radius:18px; padding:22px; box-shadow:0 4px 16px rgba(46,125,50,.12);
           border-top:5px solid #66BB6A; height:100%;}
    .card h4 {margin:.2rem 0; color:#2E7D32;}
    .stat {background:linear-gradient(135deg,#66BB6A,#2E7D32); color:#fff; border-radius:18px; padding:20px; text-align:center;}
    .stat b {font-size:2rem; display:block;} .stat span {opacity:.9;}
    .result {background:linear-gradient(135deg,#FFF8E1,#E8F5E9); border:2px solid #66BB6A; border-radius:22px;
             padding:28px; text-align:center;}
    .result .big {font-size:4rem;} .result h2 {margin:0; text-transform:capitalize;}
    .imgcap {border-radius:18px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,.15);}
    .imgcap img {width:100%; display:block;} .imgcap div {background:#fff; padding:10px 14px; font-weight:600; color:#2E7D32;}
    .stButton>button, .stFormSubmitButton>button {width:100%; background:linear-gradient(90deg,#43A047,#2E7D32); color:#fff;
             border:none; border-radius:12px; padding:.7rem; font-weight:600;}
    .stButton>button:hover {transform:translateY(-1px); box-shadow:0 6px 16px rgba(46,125,50,.4); color:#fff;}
    </style>""", unsafe_allow_html=True)
    st.sidebar.markdown("## 🌾 Smart Crop Advisor\nAI-powered crop recommendations for smarter farming.")

@st.cache_data
def img64(name):
    return base64.b64encode((ROOT / "assets" / name).read_bytes()).decode()

def hero(title, sub, image="hero_sunrise.jpg"):
    st.markdown(f"""<div class="hero" style="background-image:linear-gradient(90deg,rgba(0,40,0,.55),rgba(0,0,0,.05)),
    url(data:image/jpeg;base64,{img64(image)})"><h1>{title}</h1><p>{sub}</p></div>""", unsafe_allow_html=True)

def photo(name, caption):
    st.markdown(f"""<div class="imgcap"><img src="data:image/jpeg;base64,{img64(name)}"><div>{caption}</div></div>""",
                unsafe_allow_html=True)

def standardize_columns(df):
    """Accepts both CSV versions: 'label'/'crop' and N,P,K / Nitrogen,Phosphorous,Potassium."""
    df = df.copy(); df.columns = [str(c).strip() for c in df.columns]
    alias = {"label": "crop", "crop": "crop", "n": "Nitrogen", "nitrogen": "Nitrogen", "p": "Phosphorous",
             "phosphorous": "Phosphorous", "phosphorus": "Phosphorous", "k": "Potassium", "potassium": "Potassium",
             "temperature": "temperature", "humidity": "humidity", "ph": "ph", "rainfall": "rainfall"}
    df = df.rename(columns={c: alias[c.lower()] for c in df.columns if c.lower() in alias})
    return df.dropna(how="all")

@st.cache_data
def load_data():
    return standardize_columns(pd.read_csv(ROOT / "data" / "Crop_recommendation.csv"))

def _load():
    m = ROOT / "models"
    return (joblib.load(m / "xg_boost_model.pkl"), joblib.load(m / "scaler.pkl"),
            joblib.load(m / "label_encoders.pkl")["crop"], json.loads((m / "metrics.json").read_text()))

@st.cache_resource(show_spinner="Training the XGBoost model for the first time…")
def load_artifacts():
    """Loads saved model files; (re)trains automatically if they are missing or incompatible."""
    try:
        return _load()
    except Exception:
        from train_model import train_and_save
        train_and_save()
        return _load()
