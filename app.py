import os
import pandas as pd
import streamlit as st
from datetime import datetime

# กำหนด Path สำหรับเก็บไฟล์ข้อมูลในฮาร์ดดิสก์
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "health_records.csv")

if not os.path.exists(DATA_DIR):
  os.makedirs(DATA_DIR)

# สร้างข้อมูลตั้งต้นรวมถึงผลตรวจล่าสุดวันที่ 22/06/2026
def init_default_data():
  records = [
      # --- ข้อมูลชุดเดิม ---
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "1. การทำงานของไต (Kidney Function)", "รายการตรวจ": "Blood Urea Nitrogen (BUN)", "ค่าที่วัดได้": "60.0", "หน่วย": "mg/dL", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "1. การทำงานของไต (Kidney Function)", "รายการตรวจ": "Creatinine", "ค่าที่วัดได้": "2.4", "หน่วย": "mg/dL", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "1. การทำงานของไต (Kidney Function)", "รายการตรวจ": "Estimated Glomerular Filtration Rate (eGFR)", "ค่าที่วัดได้": "29.0", "หน่วย": "mL/min/1.73m²", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Sodium (Na)", "ค่าที่วัดได้": "125.0", "หน่วย": "mmol/L", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Potassium (K)", "ค่าที่วัดได้": "7.7", "หน่วย": "mmol/L", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Chloride (Cl)", "ค่าที่วัดได้": "99.0", "หน่วย": "mmol/L", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Bicarbonate (CO2)", "ค่าที่วัดได้": "16.0", "หน่วย": "mmol/L", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Calcium (Ca)", "ค่าที่วัดได้": "7.7", "หน่วย": "mg/dL", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Magnesium (Mg)", "ค่าที่วัดได้": "2.3", "หน่วย": "mg/dL", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Phosphorus (P)", "ค่าที่วัดได้": "5.0", "หน่วย": "mg/dL", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "3. การทำงานของตับ (Liver Function)", "รายการตรวจ": "Total Protein", "ค่าที่วัดได้": "6.5", "หน่วย": "g/dL", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "3. การทำงานของตับ (Liver Function)", "รายการตรวจ": "Albumin", "ค่าที่วัดได้": "3.9", "หน่วย": "g/dL", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "3. การทำงานของตับ (Liver Function)", "รายการตรวจ": "Globulin", "ค่าที่วัดได้": "2.6", "หน่วย": "g/dL", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "3. การทำงานของตับ (Liver Function)", "รายการตรวจ": "Aspartate Aminotransferase (AST / SGOT)", "ค่าที่วัดได้": "24.0", "หน่วย": "U/L", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "3. การทำงานของตับ (Liver Function)", "รายการตรวจ": "Alanine Aminotransferase (ALT / SGPT)", "ค่าที่วัดได้": "19.0", "หน่วย": "U/L", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "3. การทำงานของตับ (Liver Function)", "รายการตรวจ": "Alkaline Phosphatase (ALP)", "ค่าที่วัดได้": "185.0", "หน่วย": "U/L", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "3. การทำงานของตับ (Liver Function)", "รายการตรวจ": "Total Bilirubin", "ค่าที่วัดได้": "0.27", "หน่วย": "mg/dL", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "26/10/2025 19:13:00", "หมวดหมู่": "3. การทำงานของตับ (Liver Function)", "รายการตรวจ": "Direct Bilirubin", "ค่าที่วัดได้": "0.12", "หน่วย": "mg/dL", "สถานะ": "ปกติ"},

      # --- ผลตรวจใหม่วันที่ 22/06/2026 จากโรงพยาบาลลานนา ---
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "1. การทำงานของไต (Kidney Function)", "รายการตรวจ": "Blood Urea Nitrogen (BUN)", "ค่าที่วัดได้": "75", "หน่วย": "mg/dL", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "1. การทำงานของไต (Kidney Function)", "รายการตรวจ": "Creatinine", "ค่าที่วัดได้": "3.3", "หน่วย": "mg/dL", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "1. การทำงานของไต (Kidney Function)", "รายการตรวจ": "Estimated Glomerular Filtration Rate (eGFR)", "ค่าที่วัดได้": "20", "หน่วย": "mL/min/1.73m²", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Sodium (Na)", "ค่าที่วัดได้": "139", "หน่วย": "mmol/L", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Potassium (K)", "ค่าที่วัดได้": "5.0", "หน่วย": "mmol/L", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Chloride (Cl)", "ค่าที่วัดได้": "107", "หน่วย": "mmol/L", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "2. เกลือแร่ในเลือด (Electrolytes)", "รายการตรวจ": "Bicarbonate (CO2)", "ค่าที่วัดได้": "19", "หน่วย": "mmol/L", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "4. ไขมันและเบาหวานในเลือด (Lipid & Glucose)", "รายการตรวจ": "Cholesterol (Total)", "ค่าที่วัดได้": "122", "หน่วย": "mg/dL", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "4. ไขมันและเบาหวานในเลือด (Lipid & Glucose)", "รายการตรวจ": "Triglycerides", "ค่าที่วัดได้": "97", "หน่วย": "mg/dL", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "4. ไขมันและเบาหวานในเลือด (Lipid & Glucose)", "รายการตรวจ": "HDL Cholesterol", "ค่าที่วัดได้": "42", "หน่วย": "mg/dL", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "4. ไขมันและเบาหวานในเลือด (Lipid & Glucose)", "รายการตรวจ": "LDL Cholesterol", "ค่าที่วัดได้": "61.6", "หน่วย": "mg/dL", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "4. ไขมันและเบาหวานในเลือด (Lipid & Glucose)", "รายการตรวจ": "Fast Blood Sugar (FBS)", "ค่าที่วัดได้": "177", "หน่วย": "mg/dL", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "Hemoglobin (Hb)", "ค่าที่วัดได้": "8.2", "หน่วย": "g/dL", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "Hematocrit (Hct)", "ค่าที่วัดได้": "24", "หน่วย": "%", "สถานะ": "ต่ำ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "White Blood Cell Count (WBC)", "ค่าที่วัดได้": "8290", "หน่วย": "cells/cu.mm.", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "Platelet Count", "ค่าที่วัดได้": "217000", "หน่วย": "/cu.mm", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "Neutrophil", "ค่าที่วัดได้": "66", "หน่วย": "%", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "Lymphocyte", "ค่าที่วัดได้": "22", "หน่วย": "%", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "Monocyte", "ค่าที่วัดได้": "5", "หน่วย": "%", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "Eosinophil", "ค่าที่วัดได้": "7", "หน่วย": "%", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "MCV", "ค่าที่วัดได้": "83", "หน่วย": "fl", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "MCH", "ค่าที่วัดได้": "28.5", "หน่วย": "pg", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "MCHC", "ค่าที่วัดได้": "34.2", "หน่วย": "gm/dl", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "RDW cv", "ค่าที่วัดได้": "13.8", "หน่วย": "%", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "RBC Morphology", "ค่าที่วัดได้": "Normal", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "5. ความสมบูรณ์ของเม็ดเลือด (CBC)", "รายการตรวจ": "WBC Morphology", "ค่าที่วัดได้": "Normal", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:21:00", "หมวดหมู่": "7. โรคติดเชื้อและภูมิคุ้มกัน (Serology)", "รายการตรวจ": "Hbs Antigen (HBsAg)", "ค่าที่วัดได้": "Negative(0.19)", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Color", "ค่าที่วัดได้": "Yellow", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Transparency (urine)", "ค่าที่วัดได้": "Clear", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Specific gravity (urine)", "ค่าที่วัดได้": "1.009", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "pH", "ค่าที่วัดได้": "6", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Glucose (urine)", "ค่าที่วัดได้": "Negative", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Ketone (urine)", "ค่าที่วัดได้": "Negative", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Protein (urine)", "ค่าที่วัดได้": "2+", "หน่วย": "", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Blood (urine)", "ค่าที่วัดได้": "2+", "หน่วย": "", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Bile / Bilirubin (urine)", "ค่าที่วัดได้": "Negative", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Urobilinogen (urine)", "ค่าที่วัดได้": "Negative", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Urine Nitrite", "ค่าที่วัดได้": "Negative", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "WBC (urine)", "ค่าที่วัดได้": "0-1", "หน่วย": "cells/HPF", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "RBC (urine)", "ค่าที่วัดได้": "3-5", "หน่วย": "cells/HPF", "สถานะ": "ผิดปกติ / สูง"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Casts/LPF (urine)", "ค่าที่วัดได้": "Negative", "หน่วย": "", "สถานะ": "ปกติ"},
      {"วันที่ตรวจ": "22/06/2026 09:36:00", "หมวดหมู่": "6. ผลตรวจปัสสาวะ (Urinalysis)", "รายการตรวจ": "Crystal (urine)", "ค่าที่วัดได้": "Negative", "หน่วย": "", "สถานะ": "ปกติ"},
  ]
  return pd.DataFrame(records)

def load_data():
  if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, dtype=str)
    if "วันที่ตรวจ" in df.columns:
      df["วันที่ตรวจ_dt"] = pd.to_datetime(df["วันที่ตรวจ"], errors="coerce")
      df = df.sort_values(by="วันที่ตรวจ_dt", ascending=True).reset_index(drop=True)
      df = df.drop(columns=["วันที่ตรวจ_dt"])
    return df
  else:
    df_default = init_default_data()
    df_default.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    return df_default

def save_data(df):
  df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

st.set_page_config(page_title="ระบบบันทึกผลตรวจสุขภาพ", page_icon="🩺", layout="wide")

st.title("🩺 ระบบบันทึกและวิเคราะห์ผลตรวจสุขภาพ (Medical Lab Tracker)")
st.caption("บันทึกข้อมูล จัดเก็บปลอดภัยบน Harddisk | รองรับทั้งตัวเลขและข้อความ (Negative, Positive, 2+, Normal)")

df = load_data()

# ฐานข้อมูล 7 หมวดหมู่หลักแบบครบถ้วนสมบูรณ์
if "test_database" not in st.session_state:
  st.session_state["test_database"] = {
      "1. การทำงานของไต (Kidney Function)": {
          "Blood Urea Nitrogen (BUN)": {"unit": "mg/dL", "min": 6.0, "max": 20.0},
          "Creatinine": {"unit": "mg/dL", "min": 0.70, "max": 1.20},
          "Estimated Glomerular Filtration Rate (eGFR)": {"unit": "mL/min/1.73m²", "min": 60.0, "max": 120.0},
          "Uric Acid": {"unit": "mg/dL", "min": 3.4, "max": 7.0},
      },
      "2. เกลือแร่ในเลือด (Electrolytes)": {
          "Sodium (Na)": {"unit": "mmol/L", "min": 136.0, "max": 145.0},
          "Potassium (K)": {"unit": "mmol/L", "min": 3.5, "max": 5.0},
          "Chloride (Cl)": {"unit": "mmol/L", "min": 98.0, "max": 107.0},
          "Bicarbonate (CO2)": {"unit": "mmol/L", "min": 22.0, "max": 29.0},
          "Calcium (Ca)": {"unit": "mg/dL", "min": 8.5, "max": 10.5},
          "Magnesium (Mg)": {"unit": "mg/dL", "min": 1.7, "max": 2.2},
          "Phosphorus (P)": {"unit": "mg/dL", "min": 2.5, "max": 4.5},
      },
      "3. การทำงานของตับ (Liver Function)": {
          "Total Protein": {"unit": "g/dL", "min": 6.0, "max": 8.3},
          "Albumin": {"unit": "g/dL", "min": 3.5, "max": 5.0},
          "Globulin": {"unit": "g/dL", "min": 2.3, "max": 3.5},
          "Total Bilirubin": {"unit": "mg/dL", "min": 0.2, "max": 1.2},
          "Direct Bilirubin": {"unit": "mg/dL", "min": 0.0, "max": 0.3},
          "Aspartate Aminotransferase (AST / SGOT)": {"unit": "U/L", "min": 0.0, "max": 40.0},
          "Alanine Aminotransferase (ALT / SGPT)": {"unit": "U/L", "min": 0.0, "max": 41.0},
          "Alkaline Phosphatase (ALP)": {"unit": "U/L", "min": 40.0, "max": 129.0},
      },
      "4. ไขมันและเบาหวานในเลือด (Lipid & Glucose)": {
          "Cholesterol (Total)": {"unit": "mg/dL", "min": 0.0, "max": 200.0},
          "Triglycerides": {"unit": "mg/dL", "min": 0.0, "max": 150.0},
          "HDL Cholesterol": {"unit": "mg/dL", "min": 40.0, "max": 60.0},
          "LDL Cholesterol": {"unit": "mg/dL", "min": 0.0, "max": 130.0},
          "Fast Blood Sugar (FBS)": {"unit": "mg/dL", "min": 70.0, "max": 100.0},
          "HbA1c": {"unit": "%", "min": 4.0, "max": 6.0},
      },
      "5. ความสมบูรณ์ของเม็ดเลือด (CBC)": {
          "Hemoglobin (Hb)": {"unit": "g/dL", "min": 12.0, "max": 16.0},
          "Hematocrit (Hct)": {"unit": "%", "min": 36.0, "max": 48.0},
          "White Blood Cell Count (WBC)": {"unit": "cells/cu.mm.", "min": 5000.0, "max": 10000.0},
          "Platelet Count": {"unit": "/cu.mm", "min": 140000.0, "max": 440000.0},
          "Neutrophil": {"unit": "%", "min": 45.0, "max": 74.0},
          "Lymphocyte": {"unit": "%", "min": 16.0, "max": 45.0},
          "Monocyte": {"unit": "%", "min": 4.0, "max": 10.0},
          "Eosinophil": {"unit": "%", "min": 1.0, "max": 7.0},
          "MCV": {"unit": "fl", "min": 80.0, "max": 96.0},
          "MCH": {"unit": "pg", "min": 27.0, "max": 32.0},
          "MCHC": {"unit": "gm/dl", "min": 30.0, "max": 35.0},
          "RDW cv": {"unit": "%", "min": 11.6, "max": 14.5},
          "RBC Morphology": {"unit": "", "min": 0.0, "max": 0.0},
          "WBC Morphology": {"unit": "", "min": 0.0, "max": 0.0},
      },
      "6. ผลตรวจปัสสาวะ (Urinalysis)": {
          "Color": {"unit": "", "min": 0.0, "max": 0.0},
          "Transparency (urine)": {"unit": "", "min": 0.0, "max": 0.0},
          "Specific gravity (urine)": {"unit": "", "min": 1.00, "max": 1.03},
          "pH": {"unit": "", "min": 4.5, "max": 8.0},
          "Glucose (urine)": {"unit": "", "min": 0.0, "max": 0.0},
          "Ketone (urine)": {"unit": "", "min": 0.0, "max": 0.0},
          "Protein (urine)": {"unit": "", "min": 0.0, "max": 0.0},
          "Blood (urine)": {"unit": "", "min": 0.0, "max": 0.0},
          "Bile / Bilirubin (urine)": {"unit": "", "min": 0.0, "max": 0.0},
          "Urobilinogen (urine)": {"unit": "", "min": 0.0, "max": 0.0},
          "Urine Nitrite": {"unit": "", "min": 0.0, "max": 0.0},
          "WBC (urine)": {"unit": "cells/HPF", "min": 0.0, "max": 5.0},
          "RBC (urine)": {"unit": "cells/HPF", "min": 0.0, "max": 2.0},
          "Casts/LPF (urine)": {"unit": "", "min": 0.0, "max": 0.0},
          "Crystal (urine)": {"unit": "", "min": 0.0, "max": 0.0},
      },
      "7. โรคติดเชื้อและภูมิคุ้มกัน (Serology)": {
          "Hbs Antigen (HBsAg)": {"unit": "", "min": 0.0, "max": 0.0},
      }
  }

test_database = st.session_state["test_database"]

# --- ส่วนรับข้อมูลด้านซ้าย (Sidebar) ปกติ ---
st.sidebar.header("📝 โหมดบันทึกผลตรวจยกชุด (รายหมวด)")

check_date = st.sidebar.date_input("วันที่ตรวจ (ใช้ร่วมกันทั้งหมดในรอบนี้)")
check_time = st.sidebar.time_input("เวลาตรวจ")

selected_category = st.sidebar.selectbox("เลือกหมวดหมู่ที่ต้องการป้อน", list(test_database.keys()))

st.sidebar.markdown("---")
st.sidebar.subheader(f"📋 กรอกค่าผลตรวจ: {selected_category}")
st.sidebar.caption("รองรับทั้งตัวเลขและข้อความ เช่น Negative, 2+, Normal (เว้นว่างไว้ถ้าไม่มีผลตรวจ)")

batch_inputs = {}
for test_name, info in test_database[selected_category].items():
  val = st.sidebar.text_input(
      f"{test_name} ({info['unit']})" if info['unit'] else f"{test_name}",
      value="",
      key=f"input_{selected_category}_{test_name}"
  )
  batch_inputs[test_name] = val

if st.sidebar.button("💾 บันทึกข้อมูลทั้งหมวดหมู่ทีเดียว", type="primary"):
  datetime_str = f"{check_date} {check_time}"
  new_rows = []
  
  for test_name, val in batch_inputs.items():
    if val.strip() != "":
      info = test_database[selected_category][test_name]
      status = "ปกติ"
      try:
        num_val = float(val)
        min_v = info["min"]
        max_v = info["max"]
        if min_v != max_v:
          if num_val < min_v:
            status = "ต่ำ"
          elif num_val > max_v:
            status = "ผิดปกติ / สูง"
      except ValueError:
        if "positive" in val.lower() or "+" in val:
          status = "ผิดปกติ / สูง"
        else:
          status = "ปกติ"
        
      new_rows.append({
          "วันที่ตรวจ": datetime_str,
          "หมวดหมู่": selected_category,
          "รายการตรวจ": test_name,
          "ค่าที่วัดได้": val,
          "หน่วย": info["unit"],
          "สถานะ": status,
      })

  if new_rows:
    df_new = pd.DataFrame(new_rows)
    df = pd.concat([df, df_new], ignore_index=True)
    save_data(df)
    st.sidebar.success(f"บันทึกสำเร็จ {len(new_rows)} รายการ! 🎉")
    st.rerun()
  else:
    st.sidebar.warning("⚠️ กรุณากรอกค่าผลตรวจอย่างน้อย 1 รายการ")

# --- ส่วนเพิ่มรายการตรวจใหม่ใน Sidebar ---
st.sidebar.markdown("---")
st.sidebar.subheader("➕ เพิ่มรายการตรวจใหม่")
with st.sidebar.form("add_test_form"):
  new_cat = st.selectbox("เลือกหมวดหมู่", list(test_database.keys()))
  new_tname = st.text_input("ชื่อรายการตรวจใหม่")
  new_unit = st.text_input("หน่วย (เช่น mg/dL)")
  c_min = st.number_input("ค่าขั้นต่ำ (Min)", value=0.0, format="%.2f")
  c_max = st.number_input("ค่าขั้นสูง (Max)", value=100.0, format="%.2f")
  
  submitted = st.form_submit_button("➕ บันทึกรายการตรวจใหม่")
  if submitted:
    if new_tname:
      test_database[new_cat][new_tname] = {"unit": new_unit, "min": c_min, "max": c_max}
      st.success(f"เพิ่มรายการ '{new_tname}' สำเร็จ!")
      st.rerun()
    else:
      st.error("กรุณากรอกชื่อรายการตรวจ")

# --- ส่วนแสดงผลข้อมูลหลักด้านขวา ---
col1, col2, col3 = st.columns(3)
with col1:
  st.metric(label="บันทึกทั้งหมดในระบบ", value=f"{len(df)} รายการ")
with col2:
  st.metric(label="สถานที่จัดเก็บ", value="Harddisk (Local)")
with col3:
  st.metric(label="สถานะระบบ", value="พร้อมใช้งาน (7 หมวดหมู่เต็มรูปแบบ)")

st.markdown("---")

if not df.empty:
  st.subheader("📈 กราฟแสดงแนวโน้มผลตรวจสุขภาพตามกาลเวลา")
  all_recorded_tests = df["รายการตรวจ"].unique().tolist()
  selected_chart_test = st.selectbox("เลือกรายการตรวจที่ต้องการดูแนวโน้มกราฟ:", all_recorded_tests)

  chart_df = df[df["รายการตรวจ"] == selected_chart_test].copy()
  chart_df["วันที่ตรวจ_dt"] = pd.to_datetime(chart_df["วันที่ตรวจ"], errors="coerce")
  chart_df = chart_df.sort_values("วันที่ตรวจ_dt")

  if len(chart_df) > 0:
    numeric_chart_df = chart_df.copy()
    numeric_chart_df["ค่าตัวเลข"] = pd.to_numeric(numeric_chart_df["ค่าที่วัดได้"], errors="coerce")
    numeric_chart_df = numeric_chart_df.dropna(subset=["ค่าตัวเลข"])
    
    if len(numeric_chart_df) > 0:
      chart_data = numeric_chart_df.set_index("วันที่ตรวจ")[["ค่าตัวเลข"]]
      st.line_chart(chart_data, use_container_width=True)
    else:
      st.info("ℹ️ รายการนี้เก็บผลลัพธ์เป็นข้อความ จึงไม่แสดงกราฟเส้นตัวเลขครับ")

  st.markdown("---")
  st.subheader("📋 ประวัติการตรวจสุขภาพและการจัดการข้อมูล")
  st.dataframe(df, use_container_width=True)

  st.markdown("#### 🛠️ จัดการรายการ (แก้ไข หรือ ลบ)")
  with st.expander("คลิกเพื่อเปิดเมนู แก้ไข / ลบ รายการข้อมูล"):
    row_indices = df.index.tolist()
    selected_row = st.selectbox(
        "เลือกรายการที่ต้องการจัดการ:",
        row_indices,
        format_func=lambda x: f"ลำดับ {x} | {df.loc[x, 'วันที่ตรวจ']} | {df.loc[x, 'รายการตรวจ']} = {df.loc[x, 'ค่าที่วัดได้']} {df.loc[x, 'หน่วย']}"
    )

    if selected_row is not None:
      col_edit1, col_edit2 = st.columns(2)
      with col_edit1:
        st.markdown("**แก้ไขค่าของรายการนี้**")
        current_val = str(df.loc[selected_row, "ค่าที่วัดได้"])
        new_val = st.text_input("ปรับแก้ค่าที่วัดได้ใหม่", value=current_val)

        if st.button("💾 บันทึกการแก้ไข"):
          df.loc[selected_row, "ค่าที่วัดได้"] = new_val
          save_data(df)
          st.success("อัปเดตข้อมูลเรียบร้อยแล้ว!")
          st.rerun()

      with col_edit2:
        st.markdown("**ลบรายการนี้ออกจากระบบ**")
        st.write("")
        st.write("")
        if st.button("🗑️ ลบรายการนี้ทันที", type="primary"):
          df = df.drop(selected_row).reset_index(drop=True)
          save_data(df)
          st.success("ลบรายการเรียบร้อยแล้ว!")
          st.rerun()

  st.markdown("---")
  if st.button("⚠️ ล้างข้อมูลทั้งหมดในระบบ (Reset ทั้งหมด)"):
    if os.path.exists(DATA_FILE):
      os.remove(DATA_FILE)
    st.success("ล้างข้อมูลทั้งหมดเรียบร้อยแล้ว!")
    st.rerun()
else:
  st.info("ยังไม่มีข้อมูลในระบบ")

# --- [ย้ายมาไว้ด้านขวาล่างสุดของหน้าเว็บ] ส่วนจัดการระบบ Backup และ Restore ---
st.markdown("---")
st.subheader("🛡️ ระบบสำรองและกู้คืนข้อมูล (Backup & Restore)")
col_bk1, col_bk2 = st.columns(2)

with col_bk1:
  st.markdown("**1. ดาวน์โหลดข้อมูลเก็บไว้ในเครื่อง**")
  if not df.empty:
    csv_data = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="📥 ดาวน์โหลดไฟล์ Backup (CSV)",
        data=csv_data,
        file_name=f"health_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="คลิกเพื่อเซฟไฟล์ข้อมูลทั้งหมดเก็บไว้ในเครื่อง"
    )
  else:
    st.info("ยังไม่มีข้อมูลให้ดาวน์โหลด")

with col_bk2:
  st.markdown("**2. กู้คืนข้อมูลจากไฟล์ CSV เก่า**")
  uploaded_file = st.file_uploader("เลือกไฟล์ CSV สำหรับกู้คืน", type=["csv"], key="restore_uploader")
  if uploaded_file is not None:
    if st.button("🔄 ยืนยันการกู้คืนข้อมูลทับระบบเดิม"):
      try:
        restored_df = pd.read_csv(uploaded_file, dtype=str)
        save_data(restored_df)
        st.success("กู้คืนข้อมูลสำเร็จ! ระบบกำลังรีโหลด...")
        st.rerun()
      except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")