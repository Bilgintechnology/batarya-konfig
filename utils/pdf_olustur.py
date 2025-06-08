from fpdf import FPDF
import os

def temizle_unicode(metin):
    # Latin-1 (ISO-8859-1) dışındaki karakterleri kaldırır
    return metin.encode("latin-1", "ignore").decode("latin-1")

def pdf_olustur(text):
    text = temizle_unicode(text)  # Burada metni temizliyoruz

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.splitlines():
        pdf.cell(200, 10, txt=line, ln=True)

    dosya_path = os.path.join("pdf_dosyalar", "batarya_sonuc.pdf")
    os.makedirs("pdf_dosyalar", exist_ok=True)
    pdf.output(dosya_path)
    return dosya_path
