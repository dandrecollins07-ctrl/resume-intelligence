import { useState } from 'react';
import { getScoreColor } from './utils/scoreColors';
import AnalyticsDashboard from "./components/AnalyticsDashboard";

function App() {
  const [jdText, setJdText] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [result, setResult] = useState(null); // holds the /score response once we get one back

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jdText);

    const response = await fetch("http://localhost:8000/score", {
      method: "POST",
      body: formData,
    });

    const data = await response.json(); // renamed from "result" to avoid shadowing the state variable
    setResult(data); // actually save it to state so the UI re-renders with real data
  };

  return (
    // single root wrapper — JSX only allows one top-level element
    <div>
      <textarea
        value={jdText}
        onChange={(e) => setJdText(e.target.value)}
      />

      <input
        type="file"
        onChange={(e) => setResumeFile(e.target.files[0])}
      />

      <button onClick={handleSubmit}>Test</button>

      {/* Only render this block once result is populated —
          reading result.keyword before that would crash on null */}
      {result && (
        <div>
          <div className={getScoreColor(result.keyword.match_percent)}>
            Keyword Match: {result.keyword.match_percent.toFixed(1)}%
          </div>

          <div className={getScoreColor(result.semantic * 100)}>
            Semantic Match: {(result.semantic * 100).toFixed(1)}%
          </div>

          <div>
            <h3>Missing Skills:</h3>
            {result.keyword.missing_keywords.map((skill, i) => (
              <span key={i} style={{ marginRight: '8px' }}>
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;