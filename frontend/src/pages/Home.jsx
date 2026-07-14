// pages/Home.jsx
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#0B0F14] text-[#EDEEF0] flex flex-col items-center justify-center px-6">
      <div className="max-w-xl text-center">
        <p className="font-mono text-xs tracking-widest text-[#D9A441] mb-4 uppercase">
          Signal vs. Noise
        </p>
        <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
          Your resume says a lot.<br />Does it say the right things?
        </h1>
        <p className="text-[#9AA3AD] mb-10 text-lg">
          Paste a job description, upload your resume, and get a real match score — keyword overlap and semantic similarity, measured, not guessed.
        </p>
        <button
          onClick={() => navigate('/score')}
          className="bg-[#D9A441] hover:bg-[#c4922f] text-[#0B0F14] font-semibold px-8 py-3 rounded-md transition-colors"
        >
          Score my resume
        </button>
      </div>
    </div>
  );
}

export default Home;