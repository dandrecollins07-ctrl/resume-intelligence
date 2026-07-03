import { useState, useEffect } from 'react';

function App() {
  const [jdText, setJdText] = useState('');
  const [resumeFile, setResumeFile] = useState(null);


  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jdText);

    const response = await fetch("http://localhost:8000/score", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();
    console.log(result);
  }
  }
  return (
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
    </div>
  );
export default App;