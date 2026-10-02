# 🌾 Smart Crop Advisor
Multipage Streamlit app that recommends the best crop from soil nutrients (N, P, K, pH) and weather (temperature, humidity, rainfall) using an XGBoost model.

## Run locally (VS Code terminal / cmd)
```
python -m venv .venv
.venv\Scripts\activate        # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python train_model.py         # trains XGBoost and creates the models/ files
streamlit run app.py
```
(If you skip `train_model.py`, the app trains the model automatically the first time it opens.)

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repo (include the `models/` folder after running `train_model.py`).
2. Go to share.streamlit.io, click **Create app**, choose the repo, branch `main`, main file `app.py`, then **Deploy**.

## Structure
`app.py` home · `pages/` 4 inner pages · `utils.py` theme + helpers · `train_model.py` pipeline from the notebook · `data/` dataset · `assets/` images · `models/` saved model files
