# AI Resume-Job Matcher

An NLP-powered web application that compares a resume with a job description and provides a job-specific compatibility analysis.

The application accepts PDF and DOCX resumes, extracts their text, identifies technical skills, compares them with skills found in a job description, calculates skill-match and text-similarity scores, and displays the results through a simple web interface.

## Features

- Upload resumes in PDF or DOCX format
- Extract text from PDF resumes using PyPDF
- Extract text from DOCX resumes using python-docx
- Detect technical skills from resume and job-description text
- Compare resume skills with job requirements
- Display matched skills
- Display missing skills
- Calculate a skill-match percentage
- Calculate NLP text similarity using TF-IDF and cosine similarity
- Generate an overall job-match score
- Interactive browser-based frontend
- Resume file selection with a compact remove (`×`) control
- FastAPI backend with interactive API documentation

## How It Works

```text
Resume (PDF/DOCX)
        |
        v
   Text Extraction
        |
        v
    Skill Extraction
        |
        +----------------------+
        |                      |
        v                      v
 Resume Skills          Job Description
                               |
                               v
                        Job Skill Extraction
                               |
                               v
                       Skill Matching
                               |
                    +----------+----------+
                    |                     |
                    v                     v
              Skill Match          TF-IDF Similarity
                    |                     |
                    +----------+----------+
                               |
                               v
                       Overall Match Score
                               |
                               v
              Matched Skills + Missing Skills
```

## Current Scoring Method

The current implementation calculates two scores:

### 1. Skill Match Score

Skills are extracted from both the resume and job description. The score is calculated from the proportion of job-description skills that are also present in the resume.

```text
Skill Match Score =
Matched Job Skills / Total Job Skills × 100
```

### 2. NLP Similarity Score

The resume and job description are converted into TF-IDF vectors and compared using cosine similarity.

```text
TF-IDF → Vector Representation → Cosine Similarity
```

### 3. Overall Match Score

The current implementation combines the two scores using:

```text
Overall Score =
60% Skill Match
+
40% NLP Similarity
```

This scoring approach is part of the current version and can be improved as the project evolves.

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### NLP / Machine Learning
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- Regular-expression-based skill extraction

### Document Processing
- PyPDF
- python-docx

### Frontend
- HTML
- CSS
- JavaScript

## API Endpoints

### `GET /`

Returns a basic API status response.

### `POST /upload-resume`

Accepts a PDF or DOCX resume and returns extracted text and detected skills.

### `POST /match-job`

Accepts resume text and a job description and returns skill matching and similarity results.

### `POST /analyze-resume`

Accepts a resume file and job description together and returns the complete matching analysis used by the frontend.

Interactive API documentation is available through FastAPI at:

```text
http://127.0.0.1:8000/docs
```

## Project Structure

```text
ai-resume-job-matcher/
│
├── backend/
│   ├── analyzer.py
│   └── main.py
│
├── frontend/
│   └── index.html
│
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-resume-job-matcher
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install fastapi uvicorn python-multipart pypdf python-docx scikit-learn
```

## Running the Backend

From the project root, run:

```bash
python -m uvicorn backend.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Using the Frontend

1. Start the FastAPI backend.
2. Open `frontend/index.html` in a browser.
3. Select a PDF or DOCX resume.
4. Paste the target job description.
5. Click **Analyze Resume**.
6. Review the overall match score.
7. Review the skill-match and NLP-similarity scores.
8. Review matched and missing skills.

## Example Output

The dashboard provides:

- **Resume Match Score**
- **Skill Match**
- **NLP Similarity**
- **Matched Skills**
- **Missing Skills**

The match score is job-specific because the system evaluates the uploaded resume against the particular job description provided by the user.

## Current Limitations

The current version uses a predefined technical skill list and exact skill-name matching. It also uses TF-IDF for textual similarity.

Therefore, related terms or synonyms may not always be recognized as the same skill. For example, different ways of describing the same technology may not receive a match unless both terms are represented in the current skill vocabulary.

The DOCX extraction currently processes document paragraphs; information stored only inside DOCX tables is not explicitly handled by the current implementation.

## Planned Improvements

- Skill normalization and synonym detection
- Better handling of technology aliases such as ML/NLP
- Required vs. preferred skill weighting
- Improved semantic similarity
- More robust resume analysis
- Personalized missing-skill recommendations
- Resume improvement suggestions
- Job recommendation functionality
- Analysis history using SQLite
- Improved UI and visualization
- Deployment to a cloud platform
- Advanced NLP/LLM-based analysis

## Development Workflow

This project is being developed incrementally.

Each improvement is tested locally before being committed and pushed to GitHub.

```text
Develop
   ↓
Test
   ↓
Commit
   ↓
Push to GitHub
   ↓
Next Improvement
```

## Project Status

**In Development**

The current version provides the core resume-to-job matching pipeline. Future versions will focus on improving the intelligence and accuracy of the matching system.

## Author

**Deepa Amarnath Yadav**

B.Tech Artificial Intelligence
