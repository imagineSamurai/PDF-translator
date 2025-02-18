import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from tqdm import tqdm
import os

def translate_pdf(input_pdf_path, output_pdf_path, src_lang='en', dest_lang='ar'):
    # Open the PDF
    doc = fitz.open(input_pdf_path)
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    
    # Create a new translated PDF
    c = canvas.Canvas(output_pdf_path)
    
    for page_num in tqdm(range(len(doc)), desc="Translating Pages"):
        page = doc[page_num]
        text = page.get_text("text")
        
        if text.strip():
            translated_text = translator.translate(text)
        else:
            translated_text = ""

        # Write to new PDF
        c.drawString(50, 800, f"Page {page_num + 1}")
        y_position = 780  # Start position for text
        
        for line in translated_text.split("\n"):
            if y_position < 50:
                c.showPage()
                y_position = 800
            
            c.drawString(50, y_position, line)
            y_position -= 20
        
        c.showPage()  # Add new page for next PDF page
    
    c.save()
    print(f"Translation completed! Saved as {output_pdf_path}")

# Usage
translate_pdf("input.pdf", "translated_output.pdf")
