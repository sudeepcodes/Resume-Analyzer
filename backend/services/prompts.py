ATS_PROMPT = '''You are an ATS (Applicant Tracking System) expert specializing in resume optimization.

IMPORTANT: Return the analysis in the following strict JSON format WITHOUT ANY ADDITIONAL TEXT

Analyze this resume for ATS compatibility:
    {resume_text}

    IMPORATANT: Return the analysis in the following strict JSON format WITHOUT ANY ADDITIONAL TEXT
    
    Return the analysis in the following strict JSON format without any additional text:
    {{
      "overall": number between 0-100,
      "keywords": array of strings containing detected keywords,
      "missing_keywords": array of strings containing important missing keywords,
      "format_score": number between 0-100
    }}
    
    Example response format:
    {{
      "overall": 85,
      "keywords": ["python", "java", "node.js"],
      "missing_keywords": ["docker", "kubernetes"],
      "format_score": 90
    }}'''


JOB_MATCH = '''You are an experienced technical recruiter and job matching specialist.

IMPORTANT: Return the analysis in the following strict JSON format WITHOUT ANY ADDITIONAL TEXT

Compare this resume with the job description and analyze the match:

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    IMPORATANT: Return the analysis in the following strict JSON format WITHOUT ANY ADDITIONAL TEXT

    Return the analysis in the following strict JSON format without any additional text:
    {{
      "score": number between 0-100 representing overall match percentage,
      "matching_skills": array of strings containing skills that match the job requirements,
      "missing_skills": array of strings containing required skills that are missing,
      "recommendations": array of strings containing specific suggestions for improvement,
      "relevance": number between 0-100 representing experience relevance
    }}

    Example response format:
    {{
      "score": 75,
      "matching_skills": ["javascript", "react", "aws"],
      "missing_skills": ["python", "django"],
      "recommendations": ["Add experience with Python", "Highlight cloud deployment skills"],
      "relevance": 80
    }}
'''

RESUME_STRUCTURE_ANALYSIS = '''You are an expert resume structure analyzer focused on format and organization.

IMPORTANT: Return the analysis in the following strict JSON format WITHOUT ANY ADDITIONAL TEXT

Analyze the structure and formatting of this resume:
{resume_text}

Return the analysis in the following strict JSON format without any additional text:
    {{
      "completeness": number between 0-100 representing how complete the resume is,
      "sections_present": array of strings containing detected resume sections,
      "sections_missing": array of strings containing important missing sections,
      "suggestions": array of strings containing formatting and structure improvements,
      "readability": number between 0-100 representing how readable the resume is
    }}

    Example response format:
    {{
      "completeness": 85,
      "sections_present": ["summary", "experience", "education", "skills"],
      "sections_missing": ["projects", "certifications"],
      "suggestions": ["Add a projects section", "Make headers more prominent"],
      "readability": 90
    }}'''

RESUME_REPORT = '''You are a senior career coach and resume expert with extensive experience in talent acquisition.

    IMPORTANT: Return the analysis in the following strict JSON format WITHOUT ANY ADDITIONAL TEXT

    Analyze this resume and provide detailed feedback:

    RESUME:
    ${resume_text}

    JOB DESCRIPTION:
    ${job_description}

    ANALYSIS METRICS:
    - ATS Score: {ats_score}/100
    - Job Match Score: ${job_match_score}/100
    - Structure Score: ${structure_completeness_score}/100

    KEY FINDINGS:
    - Detected Keywords: ${analysis.atsScore.keywords.join(", ")}
    - Missing Keywords: ${analysis.atsScore.missingKeywords.join(", ")}
    - Matching Skills: ${analysis.jobMatch.matchingSkills.join(", ")}
    - Missing Skills: ${analysis.jobMatch.missingSkills.join(", ")}
    - Present Sections: ${analysis.structure.sectionsPresent.join(", ")}
    - Missing Sections: ${analysis.structure.sectionsMissing.join(", ")}

    Return a detailed analysis in the following STRICT JSON format without any other additional text:
    {{
      "overall_score": number between 0-100,
      "summary": A concise 2-3 sentence overview of the resume's fitness for the role,
      "strengths": Array of 3-5 key strengths identified in the resume,
      "weaknesses": Array of 3-5 main areas needing improvement,
      "action_items": Array of 4-6 specific, actionable steps to improve the resume,
      "improvement_plan": A structured paragraph describing the recommended approach to enhance the resume
    }}
    
    Example: {{ "overall_score": 95, "summary": "The resume is a strong fit for the role, showcasing exceptional 
    skills and experience.", "strengths": ["Expertise in data analysis", "Strong communication skills"], 
    "weaknesses": ["Lack of industry-specific knowledge", "Limited project management experience"], "action_items": [
    "Take a course on industry-specific data analysis", "Improve project management skills"], "improvement_plan": "To 
    enhance the resume, focus on gaining deeper knowledge in relevant fields and enhancing soft skills such as 
    communication." }}'''