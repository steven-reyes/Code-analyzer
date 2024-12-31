# src/modules/report_generator.py

import json
from fpdf import FPDF  # For PDF generation
import xlsxwriter      # For Excel

def generate_markdown_report(data: dict) -> str:
    """
    Generates a Markdown-formatted report from the provided data.
    Returns a string that you can save or print.
    """
    report_lines = ["# Analysis Report", ""]
    for key, value in data.items():
        report_lines.append(f"- **{key}**: {value}")
    return "\n".join(report_lines)

def generate_json_report(data: dict) -> str:
    """
    Returns a JSON string representation of the data.
    """
    return json.dumps(data, indent=2)

def generate_pdf_report(data: dict, output_path: str):
    """
    Generates a PDF using the FPDF library and saves it to output_path.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Analysis Report", ln=True)
    pdf.ln()

    for key, value in data.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)

    pdf.output(output_path)
    print(f"PDF report generated at {output_path}")

def generate_excel_report(data: dict, output_path: str):
    """
    Generates an Excel (.xlsx) report using xlsxwriter.
    """
    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet("Analysis")

    row = 0
    for key, value in data.items():
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, str(value))
        row += 1

    workbook.close()
    print(f"Excel report generated at {output_path}")
