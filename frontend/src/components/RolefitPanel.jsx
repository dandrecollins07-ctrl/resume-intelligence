import { buildCategoryBreakdown } from "../utils/skillCategories";

export default function RoleFitPanel({ presentSkills, missingSkills }) {
  const breakdown = buildCategoryBreakdown(presentSkills, missingSkills);

  return (
    <div className="grid grid-cols-3 gap-4">
      {Object.entries(breakdown).map(([category, { present, total }]) => {
        const pct = total === 0 ? 0 : Math.round((present / total) * 100);
        return (
          <div key={category} className="p-4 border rounded-lg text-center">
            <h3 className="capitalize font-semibold">{category}</h3>
            <p className="text-2xl font-bold">{pct}%</p>
            <p className="text-sm text-gray-500">{present}/{total} matched</p>
          </div>
        );
      })}
    </div>
  );
}