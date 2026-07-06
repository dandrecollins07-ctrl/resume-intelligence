import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

export default function SkillGapChart({ presentSkills, missingSkills }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    // Destroy old chart instance before redrawing (prevents memory leak / ghost charts)
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const allSkills = [...presentSkills, ...missingSkills];
    const data = allSkills.map((s) => (presentSkills.includes(s) ? 1 : 0));
    const colors = data.map((v) => (v === 1 ? "#22c55e" : "#ef4444")); // green / red

    chartRef.current = new Chart(canvasRef.current, {
      type: "bar",
      data: {
        labels: allSkills,
        datasets: [{ data, backgroundColor: colors }],
      },
      options: {
        indexAxis: "y", // makes it horizontal
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { display: false }, max: 1 }, // hide 0/1 axis, it's just present/absent
        },
      },
    });

    return () => chartRef.current?.destroy();
  }, [presentSkills, missingSkills]);

  return <canvas ref={canvasRef} height="300" />;
}