# -*- coding: utf-8 -*-
import json
import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

def create_pdf():
    base_dir = r"c:\Users\Student\Documents\aivin\K5-L3A-DAY06-LeVanHoang-2A202603357-DataIngestion"
    json_path = os.path.join(base_dir, "starter", "data", "toan_6_tap_1_va_2_gdpt2018.json")
    pdf_path = os.path.join(base_dir, "starter", "data", "toan_6_tap_1_va_2_gdpt2018.pdf")
    
    with open(json_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)
    
    font_path = r"C:\Windows\Fonts\arial.ttf"
    pdf.add_font("ArialVN", "", font_path)
    
    font_bold_path = r"C:\Windows\Fonts\arialbd.ttf"
    if os.path.exists(font_bold_path):
        pdf.add_font("ArialVN", "B", font_bold_path)
    else:
        pdf.add_font("ArialVN", "B", font_path)

    for item in pages:
        pdf.add_page()
        page_num = item["page"]
        section = item["section"]
        title = item["title"]
        text = item["text"]
        
        # Header
        pdf.set_font("ArialVN", "B", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(pdf.epw, 8, f"SỔ TAY TOÁN LỚP 6 (GDPT 2018) | CHƯƠNG: {section.upper()}", border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)
        
        # Page Title
        pdf.set_font("ArialVN", "B", 13)
        pdf.set_text_color(0, 51, 102)
        pdf.multi_cell(pdf.epw, 7, f"Trang {page_num}: {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)
        
        # Content
        pdf.set_font("ArialVN", "", 10)
        pdf.set_text_color(30, 30, 30)
        
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                pdf.ln(2)
                continue
            if line.startswith("###"):
                pdf.ln(2)
                pdf.set_font("ArialVN", "B", 11)
                pdf.set_text_color(0, 102, 153)
                pdf.multi_cell(pdf.epw, 6, line.replace("###", "").strip(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_font("ArialVN", "", 10)
                pdf.set_text_color(30, 30, 30)
            elif line.startswith("-") or line.startswith("*"):
                pdf.multi_cell(pdf.epw, 5.5, f"  {line}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                pdf.multi_cell(pdf.epw, 5.5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Footer
        pdf.set_y(-15)
        pdf.set_font("ArialVN", "", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(pdf.epw, 10, f"Trang {page_num} / {len(pages)} - Sách GDPT 2018 (CC BY-NC-SA 4.0)", border="T", align="C")

    pdf.output(pdf_path)
    print(f"Xuất file PDF thành công: {pdf_path} ({len(pages)} trang)")

if __name__ == "__main__":
    create_pdf()
