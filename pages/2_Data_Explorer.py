import streamlit as st, plotly.express as px
from utils import setup, hero, load_data, FEATURES, LABELS, GREENS

setup("Data Explorer", "📊")
hero("Data Explorer 📊", "Discover what each crop needs to flourish.", "farmer_harvest.jpg")
df = load_data()
t1, t2, t3, t4 = st.tabs(["Crop profile", "Distributions", "Correlations", "Raw data"])
with t1:
    crop = st.selectbox("Choose a crop", sorted(df.crop.unique()))
    avg, allavg = df[df.crop == crop][FEATURES].mean(), df[FEATURES].mean()
    fig = px.bar(x=[LABELS[f] for f in FEATURES] * 2, y=list(avg / allavg * 100) + [100] * 7,
                 color=[crop.title()] * 7 + ["All crops"] * 7, barmode="group",
                 color_discrete_sequence=["#2E7D32", "#F9A825"], labels={"x": "", "y": "% of the all-crop average", "color": ""})
    st.plotly_chart(fig)
    st.dataframe(df[df.crop == crop][FEATURES].describe().T.round(2))
with t2:
    f = st.selectbox("Feature", FEATURES, format_func=LABELS.get)
    st.plotly_chart(px.box(df, x="crop", y=f, color="crop", color_discrete_sequence=px.colors.sequential.Greens_r + GREENS))
with t3:
    st.plotly_chart(px.imshow(df[FEATURES].corr().round(2), text_auto=True, color_continuous_scale="YlGn", aspect="auto"))
with t4:
    st.dataframe(df)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), "crop_data.csv", "text/csv")
