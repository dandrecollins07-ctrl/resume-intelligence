// Maps each tracked skill to a category bucket for the role-fit panel
export const SKILL_CATEGORIES = {
  // Languages
  Python: "languages", JavaScript: "languages", TypeScript: "languages",
  Java: "languages", SQL: "languages", "C++": "languages",

  // Tools/Platforms
  Docker: "tools", AWS: "tools", PostgreSQL: "tools", Git: "tools",
  "REST API": "tools", FastAPI: "tools", React: "tools", Kubernetes: "tools",

  // Concepts
  "Machine Learning": "concepts", NLP: "concepts", "CI/CD": "concepts",
  "Data Structures": "concepts", "System Design": "concepts", TDD: "concepts",
};

// Falls back to "concepts" for anything not explicitly mapped
export function categorize(skill) {
  return SKILL_CATEGORIES[skill] || "concepts";
}

// presentSkills/missingSkills are string arrays
export function buildCategoryBreakdown(presentSkills, missingSkills) {
  const buckets = {
    languages: { present: 0, total: 0 },
    tools: { present: 0, total: 0 },
    concepts: { present: 0, total: 0 },
  };

  presentSkills.forEach((s) => {
    const cat = categorize(s);
    buckets[cat].present += 1;
    buckets[cat].total += 1;
  });

  missingSkills.forEach((s) => {
    const cat = categorize(s);
    buckets[cat].total += 1;
  });

  return buckets;
}