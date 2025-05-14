import streamlit as st
import pandas as pd
import csv
import io

st.title("Avid Locator Generator")

# Upload del file
uploaded_file = st.file_uploader("Carica un file CSV o Excel con 'timecode' e 'commento'", type=["txt", "pdf"])

# Input del Clip Name
clip_name = st.text_input("Clip Name", value="Mod Angelo")

if uploaded_file and clip_name:
    # Lettura file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Controllo colonne
    if "timecode" in df.columns and "commento" in df.columns:
        st.success("File caricato correttamente.")
        st.dataframe(df)

        # Generazione del file
        output = io.StringIO()
        writer = csv.writer(output, delimiter="\t")
        for _, row in df.iterrows():
            writer.writerow([clip_name, row["timecode"], "V1", "RED", row["commento"], 1])
        st.download_button(
            label="Scarica Avid Locator (.txt)",
            data=output.getvalue(),
            file_name="avid_locators.txt",
            mime="text/plain"
        )
    else:
        st.error("Il file deve contenere le colonne 'timecode' e 'commento'.")
