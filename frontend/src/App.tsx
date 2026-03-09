import { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, TerminalSquare, Search, RefreshCw, Code2, AlertCircle } from 'lucide-react';
import './App.css';

interface GenerateResponse {
  code: string;
  syntax_valid: boolean;
  video_path?: string;
}

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const { data } = await axios.post<GenerateResponse>('http://127.0.0.1:8000/generate/', {
        user_query: query
      });
      setResult(data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to connect to the Animind AI server.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setQuery('');
    setResult(null);
    setError(null);
  }

  return (
    <div className="app-container">
      <div className="bg-glow"></div>

      <motion.div
        layout
        className={`main-content ${result ? 'layout-split' : ''}`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <motion.div layout className="left-panel">
          <div className="header">
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 200, damping: 10 }}
              style={{ display: 'inline-block', marginBottom: '1rem' }}
            >
              <Sparkles size={48} color="var(--accent-color)" />
            </motion.div>
            <h1>Animind AI</h1>
            <p>Generate beautiful Manim mathematical animations from natural language.</p>
          </div>

          <form onSubmit={handleSubmit} style={{ width: '100%' }}>
            <div className="search-box glass-panel">
              <input
                type="text"
                className="search-input"
                placeholder="E.g., Visualize a sine wave transforming into a cosine wave..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
                autoFocus
              />
              <button
                type="submit"
                className="search-button"
                disabled={loading || !query.trim()}
                aria-label="Generate Animation"
              >
                {loading ? <RefreshCw size={20} className="spinner" /> : <Search size={20} />}
              </button>
            </div>
          </form>
        </motion.div>

        <AnimatePresence mode="wait">
          {(loading || error || result) && (
            <motion.div
              layout
              className="right-panel"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.4 }}
            >
              {loading && (
                <div className="loading-container glass-panel">
                  <TerminalSquare size={48} className="spinner" />
                  <motion.h3
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ repeat: Infinity, duration: 1.5 }}
                  >
                    Crafting Manim Script...
                  </motion.h3>
                </div>
              )}

              {error && (
                <div className="error-message glass-panel">
                  <AlertCircle size={24} />
                  <span>{error}</span>
                </div>
              )}

              {result && !loading && (
                <div className="result-container glass-panel">
                  <div className="result-header">
                    <h2><Code2 size={24} color="var(--accent-color)" /> Generated Manim Code</h2>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                      <span style={{
                        fontSize: '0.85rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        color: result.syntax_valid ? '#4ade80' : '#f87171'
                      }}>
                        <div style={{
                          width: '8px',
                          height: '8px',
                          borderRadius: '50%',
                          background: result.syntax_valid ? '#4ade80' : '#f87171'
                        }}></div>
                        Syntax: {result.syntax_valid ? 'Valid' : 'Invalid'}
                      </span>
                      <button
                        onClick={handleReset}
                        style={{
                          background: 'rgba(255,255,255,0.1)',
                          border: '1px solid rgba(255,255,255,0.2)',
                          padding: '0.4rem 0.8rem',
                          borderRadius: '6px',
                          color: 'white',
                          fontSize: '0.85rem',
                        }}
                      >
                        New Query
                      </button>
                    </div>
                  </div>

                  {result.video_path ? (
                    <div style={{ width: '100%', borderRadius: '8px', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.05)' }}>
                      <video
                        controls
                        autoPlay
                        loop
                        style={{ width: '100%', display: 'block' }}
                      >
                        <source src={`http://127.0.0.1:8000${result.video_path}`} type="video/mp4" />
                        Your browser does not support the video tag.
                      </ video>
                    </div>
                  ) : (
                    <div className="code-block">
                      {result.code || '# No code generated.'}
                    </div>
                  )}

                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

      </motion.div>
    </div>
  );
}

export default App;
