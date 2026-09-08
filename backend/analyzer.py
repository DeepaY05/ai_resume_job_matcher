import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Express",
    "Django",
    "Flask",
    "FastAPI",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "Natural Language Processing",
    "NLP",
    "Computer Vision",
    "Neural Networks",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "OpenCV",
    "Data Analysis",
    "Data Science",
    "Data Visualization",
    "Matplotlib",
    "Power BI",
    "Excel",
    "AWS",
    "Azure",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Linux",
    "Jupyter",
    "Google Colab",
    "VS Code",
    "REST API",
    "API",
    "JSON",
    "ONNX",
    "CUDA",
]


def extract_skills(text):
    found_skills = []

    text = text.lower()

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills
def match_job_description(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)

    missing_skills = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)

    if len(job_skills) > 0:
        skill_match_score = (len(matched_skills) / len(job_skills)) * 100
    else:
        skill_match_score = 0

    text_similarity_score = calculate_text_similarity(
        resume_text,
        job_description
    )

    overall_score = (
        (skill_match_score * 0.6) +
        (text_similarity_score * 0.4)
    )

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_score": round(skill_match_score, 2),
        "text_similarity_score": text_similarity_score,
        "overall_match_score": round(overall_score, 2)
    }
def calculate_text_similarity(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)