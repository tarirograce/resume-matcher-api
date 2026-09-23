import time
from celery import shared_task
from pypdf import PdfReader

from .models import Resume


@shared_task
def test_task(message):
    time.sleep(5)
    print(f"Task completed! Message was: {message}")
    return f"Processed: {message}"


@shared_task
def extract_resume_text(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        # The resume was deleted before the worker got to it
        return

    resume.extraction_status = Resume.ExtractionStatus.PROCESSING
    resume.save(update_fields=['extraction_status'])

    try:
        with resume.file.open('rb') as f:
            reader = PdfReader(f)
            pages = [page.extract_text() or '' for page in reader.pages]
        text = '\n'.join(pages).strip()

        if not text:
            # Scanned/image-only PDFs have no text layer to extract
            raise ValueError("No text found in PDF (it may be a scanned image).")

        resume.raw_text = text
        resume.extraction_status = Resume.ExtractionStatus.COMPLETED
        resume.extraction_error = ''
    except Exception as e:
        resume.extraction_status = Resume.ExtractionStatus.FAILED
        resume.extraction_error = str(e)

    resume.save(update_fields=['raw_text', 'extraction_status', 'extraction_error'])
