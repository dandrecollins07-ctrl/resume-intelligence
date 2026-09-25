from typing import List
"""
Maps each tracked skill (from skills.py) to a single dominant role category:
SWE, Data, Infra, or Analyst. Used to classify a JD's dominant role type
based on which category its extracted skills skew toward.
"""

SKILL_ROLE_CATEGORIES = {
    # Languages — mostly SWE, a couple lean Data
    "Python": "SWE", "JavaScript": "SWE", "TypeScript": "SWE", "Java": "SWE",
    "C++": "SWE", "C#": "SWE", "Go": "SWE", "Rust": "SWE",
    "SQL": "Data", "HTML": "SWE", "CSS": "SWE", "PHP": "SWE",
    "Ruby": "SWE", "Swift": "SWE", "Kotlin": "SWE",

    # Frameworks / Libraries — mostly SWE, ML ones go Data
    "React": "SWE", "Vue": "SWE", "Angular": "SWE", "FastAPI": "SWE",
    "Django": "SWE", "Flask": "SWE", "Node.js": "SWE", "Express": "SWE",
    "Next.js": "SWE", "Tailwind": "SWE", "Spring": "SWE",
    "TensorFlow": "Data", "PyTorch": "Data", "scikit-learn": "Data",
    "pandas": "Data", "NumPy": "Data",

    # Databases — Infra (running/managing them) not Data (analyzing with them)
    "PostgreSQL": "Infra", "MySQL": "Infra", "MongoDB": "Infra",
    "Redis": "Infra", "SQLite": "Infra", "DynamoDB": "Infra",

    # Cloud / Infra — all Infra
    "AWS": "Infra", "Azure": "Infra", "GCP": "Infra", "Docker": "Infra",
    "Kubernetes": "Infra", "Terraform": "Infra", "Jenkins": "Infra",
    "CI/CD": "Infra", "EC2": "Infra", "S3": "Infra", "Lambda": "Infra",
    "ECR": "Infra", "ECS": "Infra", "IAM": "Infra", "ALB": "Infra",
    "RDS": "Infra", "Nginx": "Infra", "Linux": "Infra", "Bash": "Infra",

    # Data / ML — Data
    "NLP": "Data", "Machine Learning": "Data", "Deep Learning": "Data",
    "TF-IDF": "Data", "Embeddings": "Data", "Data Pipeline": "Data",
    "ETL": "Data", "Pandas": "Data", "Data Visualization": "Analyst",
    "Tableau": "Analyst", "Power BI": "Analyst", "A/B Testing": "Analyst",

    # Tools / Practices — mostly SWE, a couple Infra
    "Git": "SWE", "GitHub": "SWE", "REST API": "SWE", "GraphQL": "SWE",
    "Microservices": "SWE", "Agile": "SWE", "Scrum": "SWE",
    "Unit Testing": "SWE", "TDD": "SWE", "System Design": "SWE",
    "OAuth": "SWE", "JWT": "SWE", "RBAC": "Infra", "Webhooks": "SWE",
    "gRPC": "SWE",
}


def classify_role(skills: List[str]) -> dict:
    """
    Given a list of extracted skills, returns a count and percentage
    breakdown across SWE/Data/Infra/Analyst, plus the dominant category.
    """
    counts = {"SWE": 0, "Data": 0, "Infra": 0, "Analyst": 0}

    for skill in skills:
        category = SKILL_ROLE_CATEGORIES.get(skill)
        if category:
            counts[category] += 1

    total = sum(counts.values())
    percentages = {
        cat: round((count / total) * 100, 1) if total else 0
        for cat, count in counts.items()
    }

    dominant = max(counts, key=counts.get) if total else None

    return {
        "counts": counts,
        "percentages": percentages,
        "dominant_category": dominant,
    }