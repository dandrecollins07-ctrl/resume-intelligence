// pages/ScorePage.jsx
import { useState } from 'react';
import { getScoreColor } from '../utils/scoreColors';

const API_URL = import.meta.env.VITE_API_URL;

function ScorePage() {
  const [jdText, setJdText] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!resumeFile || !jdText.trim()) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jdText);

    try {
      const response = await fetch(`${API_URL}/score`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F14] text-[#EDEEF0] px-6 py-12">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-8">Score my resume</h1>

        <label className="block text-sm text-[#9AA3AD] mb-2">Job description</label>
        <textarea
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
          rows={8}
          className="w-full bg-[#131924] border border-[#232B38] rounded-md p-3 text-[#EDEEF0] mb-6 focus:outline-none focus:border-[#D9A441]"
          placeholder="Paste the job description here..."
        />

        <label className="block text-sm text-[#9AA3AD] mb-2">Resume (PDF)</label>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setResumeFile(e.target.files[0])}
          className="w-full text-sm text-[#9AA3AD] mb-8 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-[#D9A441] file:text-[#0B0F14] file:font-semibold"
        />

        <button
          onClick={handleSubmit}
          disabled={loading || !resumeFile || !jdText.trim()}
          className="bg-[#D9A441] hover:bg-[#c4922f] disabled:opacity-40 disabled:cursor-not-allowed text-[#0B0F14] font-semibold px-6 py-3 rounded-md transition-colors"
        >
          {loading ? "Scoring..." : "Get my score"}
        </button>

        {result && (
          <div className="mt-10 space-y-6">
            <div className={`font-mono text-lg ${getScoreColor(result.keyword.match_percent)}`}>
              Keyword Match: {result.keyword.match_percent.toFixed(1)}%
            </div>

            <div className={`font-mono text-lg ${getScoreColor(result.semantic * 100)}`}>
              Semantic Match: {(result.semantic * 100).toFixed(1)}%
            </div>

            <div>
              <h3 className="text-sm text-[#9AA3AD] mb-2">Missing Skills</h3>
              <div className="flex flex-wrap gap-2">
                {result.keyword.missing_keywords.map((skill, i) => (
                  <span
                    key={i}
                    className="bg-[#131924] border border-[#232B38] rounded px-2 py-1 text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ScorePage;