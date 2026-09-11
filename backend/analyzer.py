import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "Python", "Java", "C++", "C", "JavaScript", "TypeScript",
    "HTML", "CSS", "React", "Node.js", "Express", "Django",
    "Flask", "FastAPI", "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "SQLite", "Artificial Intelligence", "Machine Learning",
    "Deep Learning", "Generative AI", "Natural Language Processing",
    "NLP", "Computer Vision", "Neural Networks", "TensorFlow",
    "PyTorch", "Scikit-learn", "Pandas", "NumPy", "OpenCV",
    "Data Analysis", "Data Science", "Data Visualization",
    "Matplotlib", "Power BI", "Excel", "AWS", "Azure",
    "Google Cloud", "Docker", "Kubernetes", "Git", "GitHub",
    "Linux", "Jupyter", "Google Colab", "VS Code", "REST API",
    "API", "JSON", "ONNX", "CUDA"
]


SKILL_ALIASES = {
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "python": ["python"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "machine learning": ["machine learning", "ml"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "natural language processing": [
        "natural language processing", "nlp"
    ],
    "computer vision": ["computer vision", "opencv"],
    "deep learning": ["deep learning"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "react": ["react", "react.js"],
    "node.js": ["node.js", "nodejs"],
    "git": ["git", "github"],
    "github": ["github"],
    "docker": ["docker"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "rest api": ["rest api", "restful api", "rest"],
    "data analysis": ["data analysis", "data analytics"]
}


CANONICAL_SKILLS = {
    "mysql": "SQL",
    "postgresql": "SQL",
    "sqlite": "SQL",
    "nlp": "Natural Language Processing",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "opencv": "Computer Vision",
    "js": "JavaScript",
    "ts": "TypeScript",
    "nodejs": "Node.js",
    "sklearn": "Scikit-learn",
    "restful api": "REST API",
    "rest": "REST API",
    "data analytics": "Data Analysis",
    "github": "Git"
}


SKILL_IMPORTANCE = {
    "python": "core",
    "java": "core",
    "javascript": "core",
    "typescript": "core",
    "machine learning": "core",
    "artificial intelligence": "core",
    "deep learning": "core",
    "natural language processing": "core",
    "computer vision": "core",
    "fastapi": "core",
    "django": "core",
    "flask": "core",
    "react": "core",
    "sql": "core",
    "pytorch": "core",
    "tensorflow": "core",

    "git": "supporting",
    "github": "supporting",
    "docker": "supporting",
    "html": "supporting",
    "css": "supporting",
    "numpy": "supporting",
    "pandas": "supporting",
    "matplotlib": "supporting",
    "rest api": "supporting"
}


def normalize_skill(skill):

    skill_key = skill.lower().strip()

    return CANONICAL_SKILLS.get(
        skill_key,
        skill
    )


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS:

        skill_key = skill.lower()

        aliases = SKILL_ALIASES.get(
            skill_key,
            [skill_key]
        )

        for alias in aliases:

            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            if re.search(pattern, text):

                canonical_skill = normalize_skill(alias)

                if canonical_skill not in found_skills:

                    found_skills.append(
                        canonical_skill
                    )

                break

    return found_skills


def calculate_text_similarity(
    resume_text,
    job_description
):

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


def generate_recommendations(
    missing_skills,
    matched_skills
):

    recommendations = []

    core_missing = []
    supporting_missing = []

    for skill in missing_skills:

        importance = SKILL_IMPORTANCE.get(
            skill.lower(),
            "supporting"
        )

        if importance == "core":
            core_missing.append(skill)

        else:
            supporting_missing.append(skill)

    if core_missing:

        recommendations.append(
            "Focus on developing these core skills: "
            + ", ".join(core_missing)
            + "."
        )

    if supporting_missing:

        recommendations.append(
            "Consider adding these supporting skills: "
            + ", ".join(supporting_missing)
            + "."
        )

    if matched_skills:

        recommendations.append(
            "Your resume already demonstrates "
            "relevant experience in: "
            + ", ".join(matched_skills)
            + "."
        )

    if not missing_skills:

        recommendations.append(
            "Your listed skills cover all the "
            "skills detected in this job description."
        )

    return recommendations


def match_job_description(
    resume_text,
    job_description
):

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    matched_skills = []
    missing_skills = []

    for job_skill in job_skills:

        if job_skill in resume_skills:

            matched_skills.append(
                job_skill
            )

        else:

            missing_skills.append(
                job_skill
            )

    total_weight = 0
    matched_weight = 0

    for skill in job_skills:

        importance = SKILL_IMPORTANCE.get(
            skill.lower(),
            "supporting"
        )

        weight = 2 if importance == "core" else 1

        total_weight += weight

        if skill in matched_skills:

            matched_weight += weight

    if total_weight > 0:

        skill_match_score = (
            matched_weight / total_weight
        ) * 100

    else:

        skill_match_score = 0

    text_similarity_score = calculate_text_similarity(
        resume_text,
        job_description
    )

    overall_score = (
        (skill_match_score * 0.6)
        +
        (text_similarity_score * 0.4)
    )

    skill_breakdown = []

    for skill in job_skills:

        importance = SKILL_IMPORTANCE.get(
            skill.lower(),
            "supporting"
        )

        status = (
            "matched"
            if skill in matched_skills
            else "missing"
        )

        skill_breakdown.append({
            "skill": skill,
            "importance": importance,
            "status": status
        })

    recommendations = generate_recommendations(
        missing_skills,
        matched_skills
    )

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_breakdown": skill_breakdown,
        "skill_match_score": round(
            skill_match_score,
            2
        ),
        "text_similarity_score": text_similarity_score,
        "overall_match_score": round(
            overall_score,
            2
        ),
        "recommendations": recommendations
    }