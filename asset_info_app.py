import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import os

@st.cache_data
def load_data():
    df = pd.read_excel("assets_data.xlsx")
    df.columns = df.columns.str.strip()
    return df

def generate_pdf(asset_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", '', fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
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

st.set_page_config(page_title="البحث عن الأصول", layout="centered")
st.title("🔍 نظام البحث عن الأصول - هيئة المساحة الجيولوجية")

asset_number = st.text_input("أدخل رقم الأصل:")
user_email = st.text_input("أدخل بريدك الإلكتروني:")

if st.button("بحث") and asset_number:
    df = load_data()
    matched_asset = df[df[df.columns[0]].astype(str) == asset_number]

    if not matched_asset.empty:
        asset_info = matched_asset.iloc[0].to_dict()
        st.success("تم العثور على الأصل!")

        for key, value in asset_info.items():
            st.write(f"**{key}**: {value}")

        pdf_file = generate_pdf(asset_info)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 تحميل تقرير PDF", f, file_name=f"Asset_{asset_number}.pdf")

        os.remove(pdf_file)
    else:
        st.error("لم يتم العثور على أصل بهذا الرقم.")
