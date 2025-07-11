import re
import json
from fpdf import FPDF


def parse_jsonlg_line(line: str):
    content_pattern = re.compile(r'("content"\s*:\s*f")((\\.|[^"\\])*)(")')
    contents_found = []

    def replace_match(m):
        idx = len(contents_found)
        # On stocke le texte capturé
        content_text = m.group(2)
        contents_found.append(content_text)
        return f'"content": "PLACEHOLDER_{idx}"'

    line_clean = content_pattern.sub(replace_match, line)

    data = json.loads(line_clean)  # parse JSON "classique"

    # Replacer les placeholders par le vrai contenu
    ph_pattern = re.compile(r'^PLACEHOLDER_(\d+)$')
    messages = data.get("messages", [])
    for msg in messages:
        c = msg.get("content", "")
        m_ph = ph_pattern.match(c)
        if m_ph:
            index = int(m_ph.group(1))
            real_content = contents_found[index]
            msg["content"] = real_content

    return data


class MyPDF(FPDF):
    pass


def build_pdf_for_data(data, pdf):
    messages = data.get("messages", [])

    dev_content = ""
    user_contents = []
    assistant_contents = []

    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "developer":
            dev_content = content
        elif role == "user":
            user_contents.append(content)
        elif role == "assistant":
            assistant_contents.append(content)

    # Developer en haut
    pdf.set_font("Arial", 'B', 14)
    pdf.multi_cell(0, 10, "DEVELOPER", align='C')
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, dev_content, align='C')
    pdf.ln(8)

    # Assistant à gauche, user à droite (exemple simpliste)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "ASSISTANT :", ln=True)
    pdf.set_font("Arial", '', 12)
    for atext in assistant_contents:
        pdf.multi_cell(0, 10, atext)
        pdf.ln(4)

    pdf.ln(6)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "USER :", ln=True)
    pdf.set_font("Arial", '', 12)
    for utext in user_contents:
        pdf.multi_cell(0, 10, utext)
        pdf.ln(4)

    # Séparateur
    pdf.ln(10)
    pdf.cell(0, 0, '-' * 80, ln=True)
    pdf.ln(10)


def jsonlg_to_pdf(input_file, output_pdf):
    pdf = MyPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = parse_jsonlg_line(line)
            build_pdf_for_data(data, pdf)

    pdf.output(output_pdf)
    print(f"PDF généré: {output_pdf}")


if __name__ == "__main__":
    jsonlg_to_pdf("input.jsonlg", "output.pdf")
