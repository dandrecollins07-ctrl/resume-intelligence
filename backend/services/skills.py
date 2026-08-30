"""
Curated technical skill list + extraction logic.
Scans resume/JD text for exact-match technical skills using word-boundary matching.
"""

import re

# Skill list: mix of languages, frameworks/tools, cloud/infra, data/ML, and concepts.
# Display casing here is what gets returned/shown — matching is case-insensitive.
SKILLS = [
    # Languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
    "SQL", "HTML", "CSS", "PHP", "Ruby", "Swift", "Kotlin",

    # Frameworks / Libraries
    "React", "Vue", "Angular", "FastAPI", "Django", "Flask", "Node.js",
    "Express", "Next.js", "Tailwind", "Spring", "TensorFlow", "PyTorch",
    "scikit-learn", "pandas", "NumPy",

    # Databases
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "DynamoDB",

    # Cloud / Infra
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins",
    "CI/CD", "EC2", "S3", "Lambda", "ECR", "ECS", "IAM", "ALB", "RDS",
    "Nginx", "Linux", "Bash",

    # Data / ML
    "NLP", "Machine Learning", "Deep Learning", "TF-IDF", "Embeddings",
    "Data Pipeline", "ETL", "Pandas", "Data Visualization", "Tableau",
    "Power BI", "A/B Testing",

    # Tools / Practices
    "Git", "GitHub", "REST API", "GraphQL", "Microservices", "Agile",
    "Scrum", "Unit Testing", "TDD", "System Design", "OAuth", "JWT",
    "RBAC", "Webhooks", "gRPC",
]

# Precompile word-boundary regex patterns once, at import time, for speed.
# re.escape handles skills with special regex chars (C++, C#).
_SKILL_PATTERNS = [
    (skill, re.compile(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", re.IGNORECASE))
    for skill in SKILLS
]


def extract_skills(text: str) -> list[str]:
    """
    Scans input text for known technical skills using word-boundary matching
    (so 'React' won't match inside 'Reaction', etc.).
    Returns skills in their canonical display casing, in the order they
    appear in SKILLS (not order of appearance in text).
    """
    if not text:
        return []

    found = []
    for skill, pattern in _SKILL_PATTERNS:
        if pattern.search(text):
            found.append(skill)

    return found