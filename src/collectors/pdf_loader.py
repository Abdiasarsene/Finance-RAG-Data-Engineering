# src/colectors/pdf_loader.py
import os
import json
import logging
import PyPDF2
from datetime import datetime, timezone
from pathlib import Path

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== DEFINE PATH ======
RAW_DATA_DIR = Path("./data/pdfs")

# ====== EXTRACT TEXT IN PDF ======
def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        text= ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfFileReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}", exc_info=True)

# ====== CONVERT FROM PDF TO JSON ======
def pdf_to_json(pdf_path: str) -> dict:
    try:
        text = extract_text_from_pdf(pdf_path)
        return {
            "source": "pdf",
            "file_name": os.path.basename(extract_text_from_pdf),
            "date_collected": datetime.now(timezone.utc).isoformat(),
            "raw&_content": text,
            "metadata":{
                "num_pages":len(PyPDF2.PdfFileReader(pdf_path).pages)
            }
        }
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}", exc_info=True)

# ====== STOCK INTO THE PATH ======
def ingest_pdfs(input_dir="./data/pdfs", output_dir=RAW_DATA_DIR):
    try:
        os.makedirs(output_dir, exist_ok=True)
        for pdf_file in Path(input_dir).glob("*.pdf"):
            doc_json = pdf_to_json(str(pdf_file))
            out_path = output_dir / f"{pdf_file.stem}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(doc_json, f, ensure_ascii=True, indent=2)
        logger.info("✅ PDF extracted and saved")
    except Exception as e:
        logger.error(f"❌ Error Detectd : {str(e)}")

# ====== MAIN BUTTOM ======
if __name__ == "__main__": 
    ingest_pdfs()