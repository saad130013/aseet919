import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import os

# Load data from CSV file
@st.cache_data
def load_data():
    csv_path = "assets_data.csv"
    if not os.path.exists(csv_path):
        st.error("⚠️ The data file 'assets_data.csv' is missing from the project folder.")
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    return df

def generate_pdf(asset_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Asset Report (Electronic Only)", ln=True, align='C')
    pdf.ln(10)

    for key, value in asset_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.ln(10)
    pdf.set_text_color(150, 0, 0)
    pdf.set_font("Arial", style='I', size=10)
    pdf.cell(200, 10, txt="This report is electronically generated and not officially approved.", ln=True)

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    return temp_pdf.name

# Main interface
st.set_page_config(page_title="Asset Lookup - SGS", layout="centered")
st.title("🔍 Asset Lookup System - Saudi Geological Survey")

asset_number = st.text_input("Enter Asset Number:")
user_email = st.text_input("Enter your email:")

if st.button("Search") and asset_number:
    df = load_data()
    if df.empty:
        st.stop()

    st.write("Available Columns:", df.columns.tolist())

    df_first_col = df.columns[0]
    df[df_first_col] = df[df_first_col].astype(str).str.strip()
    asset_number = asset_number.strip()

    st.write("Searching for asset number:", asset_number)
    st.write("Sample values in column:", df[df_first_col].head(10).tolist())

    matched_asset = df[df[df_first_col] == asset_number]

    if not matched_asset.empty:
        asset_info = matched_asset.iloc[0].to_dict()
        st.success("Asset found!")

        for key, value in asset_info.items():
            st.write(f"**{key}**: {value}")

        pdf_file = generate_pdf(asset_info)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download PDF Report", f, file_name=f"Asset_{asset_number}.pdf")

        os.remove(pdf_file)
    else:
        st.error("No asset found with this number.")
