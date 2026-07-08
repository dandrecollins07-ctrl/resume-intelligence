import { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";

function AnalyticsDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    fetch("http://localhost:8000/analytics")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch analytics");
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!data || !data.score_trend || data.score_trend.length === 0) return;

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const labels = data.score_trend.map((row) => row.day);
    const keywordScores = data.score_trend.map((row) => row.avg_kw);
    const semanticScores = data.score_trend.map((row) => row.avg_sem);

    chartInstance.current = new Chart(chartRef.current, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Avg Keyword Score",
            data: keywordScores,
            borderColor: "rgb(59, 130, 246)",
            tension: 0.2,
          },
          {
            label: "Avg Semantic Score",
            data: semanticScores,
            borderColor: "rgb(16, 185, 129)",
            tension: 0.2,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { position: "top" } },
      },
    });

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [data]);

  if (loading) return <div className="p-4">Loading analytics...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Score Trend Over Time</h2>
      {data.score_trend && data.score_trend.length > 0 ? (
        <canvas ref={chartRef}></canvas>
      ) : (
        <p className="text-gray-500">No trend data yet.</p>
      )}

      <h2 className="text-xl font-bold mt-8 mb-4">Top Missing Skills</h2>
      {data.top_missing_skills && data.top_missing_skills.length > 0 ? (
        <ul className="list-disc pl-5">
          {data.top_missing_skills.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">Not yet available — coming soon.</p>
      )}
    </div>
  );
}

export default AnalyticsDashboard;