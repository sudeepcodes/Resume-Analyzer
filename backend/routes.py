import time
import uuid
from io import BytesIO
from typing import Dict

import fitz
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from exceptions import GroqException
from services.service_factory import analyze_resume

router = APIRouter()
extracted_texts: Dict[str, Dict] = {}


@router.post('/upload')
async def upload_pdf(file: UploadFile = File(...)):
    if not (file.content_type == 'application/pdf' or file.filename.lower().endswith('.pdf')):
        raise HTTPException(status_code=400, detail='Uploaded file is not a valid pdf')

    request_id = str(uuid.uuid4())
    contents = await file.read()
    pdf_in_memory = BytesIO(contents)

    doc = fitz.open(filename=file.filename, stream=pdf_in_memory)
    text = ''
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    extracted_texts[request_id] = {
        'text': text,
        'ttl': time.time() + 5 * 60
    }
    return {
        'request_id': request_id,
        'result': {
            'filename': file.filename,
            'message': 'File uploaded successfully.'
        }

    }


@router.get('/analyze/ats/{request_id}')
async def get_ats_score(request_id: str):
    resume_text = extracted_texts.get(request_id, {}).get('text', '')
    if not resume_text:
        raise HTTPException(status_code=400,
                            detail='Please upload resume before analyzing.')
    try:
        ats_analysis_response = analyze_resume(analysis_type='ats', resume_text=resume_text)
    except GroqException:
        raise HTTPException(status_code=500,
                            detail='Internal Server Error')

    return {
        'request_id': request_id,
        'result': {
            **ats_analysis_response
        }

    }


@router.get('/analyze/resume-structure/{request_id}')
async def get_resume_structure_analysis(request_id: str):
    resume_text = extracted_texts.get(request_id, {}).get('text', '')
    if not resume_text:
        raise HTTPException(status_code=400,
                            detail='Please upload resume before analyzing.')
    try:
        structure_analysis_response = analyze_resume(analysis_type='structure', resume_text=resume_text)
    except GroqException:
        raise HTTPException(status_code=500,
                            detail='Internal Server Error')

    return {
        'request_id': request_id,
        'result': {
            **structure_analysis_response
        }

    }


class JobDescription(BaseModel):
    job_description: str


@router.post('/analyze/job-match/{request_id}')
async def get_job_match_analysis(request_id: str, job_description: str = Form(...)):
    resume_text = extracted_texts.get(request_id, {}).get('text', '')
    if not resume_text:
        raise HTTPException(status_code=400,
                            detail='Please upload resume before analyzing.')

    try:
        job_match_response = analyze_resume(analysis_type='job_match', resume_text=resume_text,
                                            job_description=job_description)
    except GroqException as ex:
        raise HTTPException(status_code=500,
                            detail='Internal Server Error')

    return {
        'request_id': request_id,
        'result': {
            **job_match_response
        }
    }
