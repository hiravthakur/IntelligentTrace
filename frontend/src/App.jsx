import { useState } from "react";
import "./App.css";
import DependencyGraph from "./components/DependencyGraph";

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [aiReport, setAiReport] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyzeFile() {
  if (!file) {
    alert("Choose a log file first");
    return;
  }

  setLoading(true);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const analysisResponse = await fetch(
      "http://127.0.0.1:8000/analyze",
      {
        method: "POST",
        body: formData,
      }
    );

    const analysisData = await analysisResponse.json();

    setAnalysis(analysisData);

    const aiFormData = new FormData();
    aiFormData.append("file", file);

    const aiResponse = await fetch(
      "http://127.0.0.1:8000/ai-report",
      {
        method: "POST",
        body: aiFormData,
      }
    );

    const aiData = await aiResponse.json();

    setAiReport(aiData);
  } catch (error) {
    console.error(error);
    alert("Failed to analyze logs");
  }

  setLoading(false);
}

  return (
    <main className="container">
      <section className="hero">
        <h1>IntelligentTrace</h1>
        <p>AI-ready operational intelligence for logs and incident analysis.</p>
      </section>

      <section className="card">
        <h2>Upload Logs</h2>
        <input
          type="file"
          accept=".log,.txt,.csv,.json"
          onChange={(event) => setFile(event.target.files[0])}
        />

        <button onClick={analyzeFile} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Incident"}
        </button>
      </section>

      {analysis && (
        <>
          <section className="grid">
            <div className="metric">
              <span>Total Events</span>
              <strong>{analysis.totalEvents}</strong>
            </div>

            <div className="metric">
              <span>Errors</span>
              <strong>{analysis.errorCount}</strong>
            </div>

            <div className="metric">
              <span>Warnings</span>
              <strong>{analysis.warnCount}</strong>
            </div>

            <div className="metric">
              <span>Most Affected</span>
              <strong>{analysis.mostAffectedService}</strong>
            </div>
          </section>

          <section className="card">
                <h2>Service Health</h2>
              <div className="service-list">
                {Object.entries(analysis.serviceCounts).map(([service, count]) => (
                  <div className="service-row" key={service}>
                    <span>{service}</span>
                    <div className="bar">
                      <div
                        className="bar-fill"
                        style={{ width: `${(count / analysis.totalEvents) * 100}%` }}
                      />
                    </div>
                    <strong>{count}</strong>
                  </div>
                ))}
              </div>
            </section>

          <section className="card">
            <h2>Likely Root Cause</h2>
            <p>{analysis.rootCause}</p>
          </section>

          {analysis.dependencies && analysis.dependencies.length > 0 && (
          <section className="card">
            <h2>Service Dependency Graph</h2>

            {analysis.cascadeDetected && (
              <p className="cascade-alert">
                Potential cascading failure detected across multiple services.
              </p>
            )}

            <DependencyGraph analysis={analysis} />
          </section>
        )}

          <section className="card">
            <h2>Incident Timeline</h2>
             <div className="timeline">
               {analysis.timeline.map((item, index) => (
                <div className="timeline-item" key={index}>
                 <span className="time">{item.timestamp}</span>
               <span className={`badge ${item.severity.toLowerCase()}`}>
               {item.severity}
               </span>
             <span className="service-tag">{item.service}</span>
        <p>{item.message}</p>
      </div>
    ))}
  </div>
          </section>
        
        {aiReport && (
  <section className="card">
    <h2>AI Incident Report</h2>

    <div className="ai-section">
      <h3>Executive Summary</h3>
      <p>{aiReport.executiveSummary}</p>
    </div>

    <div className="ai-section">
      <h3>Technical Summary</h3>
      <p>{aiReport.technicalSummary}</p>
    </div>

    <div className="ai-section">
      <h3>Likely Root Cause</h3>
      <p>{aiReport.likelyRootCause}</p>
    </div>

    <div className="ai-section">
      <h3>Recommended Actions</h3>

      <ul>
        {aiReport.recommendedActions.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  </section>
)}
        </>
      )}
    </main>
  );
}

export default App;