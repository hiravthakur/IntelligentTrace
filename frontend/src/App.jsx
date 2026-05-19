import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyzeFile() {
    if (!file) {
      alert("Choose a log file first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setAnalysis(data);
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

          <section className="card">
            <h2>Recommendations</h2>
            <ul>
              {analysis.recommendations.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </section>
        </>
      )}
    </main>
  );
}

export default App;