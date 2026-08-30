import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

const CATEGORY_COLORS = {
  SWE: "#3b82f6",      // blue
  Data: "#a855f7",     // purple
  Infra: "#f59e0b",    // amber
  Analyst: "#22c55e",  // green
};

export default function RoleClassificationPanel({ roleClassification }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  const { counts, percentages, dominant_category } = roleClassification || {};

  useEffect(() => {
    if (!canvasRef.current || !counts) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const labels = Object.keys(counts);
    const data = labels.map((cat) => counts[cat]);
    const colors = labels.map((cat) => CATEGORY_COLORS[cat]);

    chartRef.current = new Chart(canvasRef.current, {
      type: "doughnut",
      data: {
        labels,
        datasets: [{ data, backgroundColor: colors }],
      },
      options: {
        plugins: {
          legend: { position: "bottom" },
        },
      },
    });

    return () => chartRef.current?.destroy();
  }, [counts]);

  if (!roleClassification || !dominant_category) {
    return (
      <div className="p-4 border rounded-lg text-center text-gray-500">
        No role classification available for this job description.
      </div>
    );
  }

  return (
    <div className="p-4 border rounded-lg">
      <h3 className="text-lg font-semibold mb-2 text-center">
        This job description is{" "}
        <span style={{ color: CATEGORY_COLORS[dominant_category] }}>
          {percentages[dominant_category]}% {dominant_category}
        </span>
        -focused
      </h3>
      <canvas ref={canvasRef} height="250" />
    </div>
  );
}