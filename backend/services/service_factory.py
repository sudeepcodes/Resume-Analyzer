import json

from exceptions import GroqException
from globals import groq_client

from .prompts import ATS_PROMPT, RESUME_STRUCTURE_ANALYSIS, JOB_MATCH


class ResumeAnalysis:
    def __init__(self, resume_text: str, job_description: str = None):
        self.resume_text = resume_text
        self.job_description = job_description

    def analyze(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def get_groq_response(self, prompt: str):
        chat_completion = groq_client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt
            }],
            model="llama-3.2-90b-vision-preview",
            temperature=0.3
        )
        return chat_completion.choices[0].message.content


class ATSAnalysis(ResumeAnalysis):
    def analyze(self):
        ats_prompt = ATS_PROMPT.format(resume_text=self.resume_text)
        result = json.loads(self.get_groq_response(ats_prompt))
        return {
            'overall': int(result.get('overall', 0)),
            'keywords': result.get('keywords', []),
            'missing_keywords': result.get('missing_keywords', []),
            'format_score': int(result.get('format_score', 0)),
        }


class ResumeStructureAnalysis(ResumeAnalysis):
    def analyze(self):
        resume_structure_prompt = RESUME_STRUCTURE_ANALYSIS.format(resume_text=self.resume_text,
                                                                   job_description=self.job_description)
        result = json.loads(self.get_groq_response(resume_structure_prompt))
        return {
            'completeness': int(result.get('completeness', 0)),
            'sections_present': result.get('sections_present', []),
            'sections_missing': result.get('sections_missing', []),
            'suggestions': result.get('suggestions', []),
            'readability': int(result.get('readability', 0)),
        }


class JobMatch(ResumeAnalysis):
    def analyze(self):
        job_match_prompt = JOB_MATCH.format(resume_text=self.resume_text, job_description=self.job_description)
        result = json.loads(self.get_groq_response(job_match_prompt))
        return {
            'score': int(result.get('score', 0)),
            'matching_skills': result.get('matching_skills', []),
            'missing_skills': result.get('missing_skills', []),
            'recommendations': result.get('recommendations', []),
            'relevance': int(result.get('relevance', 0)),
        }


class ResumeAnalysisFactory:
    @staticmethod
    def get_analysis(analysis_type: str, resume_text: str, job_description: str = None) -> ResumeAnalysis:
        if analysis_type == "ats":
            return ATSAnalysis(resume_text=resume_text)
        elif analysis_type == "structure":
            return ResumeStructureAnalysis(resume_text=resume_text)
        elif analysis_type == 'job_match':
            return JobMatch(resume_text=resume_text, job_description=job_description)
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")


def analyze_resume(analysis_type: str, resume_text: str, job_description: str = None):
    try:
        analysis_instance = ResumeAnalysisFactory.get_analysis(analysis_type, resume_text, job_description)
        return analysis_instance.analyze()
    except Exception as ex:
        raise GroqException('Groq API failed')
