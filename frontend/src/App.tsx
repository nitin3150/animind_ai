import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import {
  Sun, ChevronDown, CornerDownLeft, ArrowUp, Code2, AlertCircle,
  Play, TrendingUp, Layers, Activity, BarChart2, Sparkles,
  RefreshCw, Share2, ExternalLink
} from 'lucide-react';
import './App.css';

interface GenerateResponse {
  code: string;
  syntax_valid: boolean;
  video_path?: string;
}

function App() {
  const [query, setQuery] = useState('');
  const [submittedQuery, setSubmittedQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (endOfMessagesRef.current) {
      endOfMessagesRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [loading, result, error]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setSubmittedQuery(query);
    setLoading(true);
    setError(null);
    setResult(null);

    // Keep query in input or clear it? Better to clear it for the next message in chat layout
    const currentQuery = query;
    setQuery('');

    try {
      const { data } = await axios.post<GenerateResponse>('http://127.0.0.1:8000/generate/', {
        user_query: currentQuery
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
    setSubmittedQuery('');
    setResult(null);
    setError(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  const isSplitView = !!submittedQuery || loading || error || result;

  return (
    <div className="app-container">
      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-left">
          <div className="logo-container" onClick={handleReset} style={{ cursor: 'pointer' }}>
            <Sparkles size={24} color="var(--accent-color)" />
            <span>Animind AI</span>
          </div>
        </div>
        <div className="nav-right">
          <button className="icon-btn">
            <Sun size={18} />
          </button>
          <div className="lang-selector">
            English <ChevronDown size={14} />
          </div>
          <span className="profile-text">Nitin Goyal</span>
          <div className="avatar">
            <span>NG</span>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      {!isSplitView ? (
        <main className="main-content hero-view">
          <div className="center-logo">
            <Sparkles size={48} color="var(--accent-color)" />
          </div>

          <h1 className="title">Animate math with Animind AI</h1>
          <p className="subtitle">Generate animations and interactive 3D math scenes from plain English.</p>

          <form onSubmit={handleSubmit} style={{ width: '100%' }}>
            <div className="search-container">
              <textarea
                className="search-input"
                placeholder="What math animation would you like to create?"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
                autoFocus
              />
              <div className="search-footer">
                <div className="search-footer-left">
                  <span className="enter-key">
                    <CornerDownLeft size={10} /> Enter
                  </span>
                  to submit
                </div>
                <div className="search-footer-right">
                  <button
                    type="submit"
                    className="submit-btn"
                    disabled={loading || !query.trim()}
                  >
                    <ArrowUp size={16} />
                  </button>
                </div>
              </div>
            </div>
          </form>

          <div className="suggestions-grid">
            <button className="suggestion-pill" onClick={() => setQuery('Demonstrate sine and cosine waves')}>
              <BarChart2 size={14} style={{ color: '#4ade80' }} /> Demonstrate sine and cosine waves
            </button>
            <button className="suggestion-pill" onClick={() => setQuery('Projectile motion')}>
              <Play size={14} style={{ color: '#f97316' }} /> Projectile motion
            </button>
            <button className="suggestion-pill" onClick={() => setQuery('Compare exponential growth vs linear growth')}>
              <TrendingUp size={14} style={{ color: '#ef4444' }} /> Compare exponential growth vs linear growth
            </button>
            <button className="suggestion-pill" onClick={() => setQuery('Slope of a tangent line')}>
              <Layers size={14} style={{ color: '#3b82f6' }} /> Slope of a tangent line
            </button>
            <button className="suggestion-pill" onClick={() => setQuery("Bayes' theorem visualization")}>
              <Activity size={14} style={{ color: '#a855f7' }} /> Bayes' theorem visualization
            </button>
            <button className="suggestion-pill" onClick={() => setQuery('Sample mean derivation')}>
              <BarChart2 size={14} style={{ color: '#06b6d4' }} /> Sample mean derivation
            </button>
          </div>
        </main>
      ) : (
        <main className="split-view">
          {/* Left Panel - Chat */}
          <div className="chat-sidebar">
            <div className="chat-messages">
              {submittedQuery && (
                <div className="user-message">
                  {submittedQuery}
                </div>
              )}

              <div className="ai-message">
                <div className="ai-avatar-name">
                  <Sparkles size={16} color="var(--accent-color)" />
                  <span>Animind AI</span>
                </div>

                {loading && (
                  <div className="loading-state">
                    <Activity size={20} className="spinner" />
                    <span>Crafting your mathematical animation...</span>
                  </div>
                )}

                {error && (
                  <div className="error-message">
                    <AlertCircle size={20} />
                    <span>{error}</span>
                  </div>
                )}

                {result && !loading && (
                  <div className="success-state">
                    <p>
                      Your animation is ready! The media player on the right shows the generated mathematical visualization.
                      You can also view the generated Manim code representation if needed.
                    </p>
                    <div className="code-fragment-btn">
                      <Code2 size={14} />
                      Generated Manim Script
                    </div>
                  </div>
                )}
              </div>
              <div ref={endOfMessagesRef} />
            </div>

            <div className="chat-input-wrapper">
              <form onSubmit={handleSubmit} style={{ width: '100%' }}>
                <div className="search-container chat-search-container">
                  <textarea
                    className="search-input"
                    placeholder="Ask a follow-up or create a new animation..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={loading}
                    autoFocus
                  />
                  <div className="search-footer">
                    <div className="search-footer-left">
                      <span className="enter-key">
                        <CornerDownLeft size={10} /> Enter
                      </span>
                      to submit
                    </div>
                    <div className="search-footer-right">
                      <button
                        type="submit"
                        className="submit-btn"
                        disabled={loading || !query.trim()}
                      >
                        <ArrowUp size={16} />
                      </button>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>

          {/* Right Panel - Media Player View */}
          <div className="media-viewer">
            <div className="media-header">
              <button className="icon-btn action-btn" onClick={() => { }}>
                <RefreshCw size={16} />
              </button>
              <div className="share-link-bar">
                <Share2 size={14} />
                <span>animind.ai/share/session-ab91-4c72</span>
              </div>
              <button className="icon-btn action-btn">
                <ExternalLink size={16} />
              </button>
            </div>

            <div className="media-content">
              {loading && !result && !error && (
                <div className="placeholder-media">
                  <Activity size={48} className="spinner" color="var(--accent-color)" />
                  <p>Compiling rendering engine...</p>
                </div>
              )}

              {!loading && !result && error && (
                <div className="placeholder-media error-media">
                  <AlertCircle size={48} color="#ef4444" />
                  <p>Failed to generate view.</p>
                </div>
              )}

              {result && !loading && (
                <div className="result-display">
                  {result.video_path ? (
                    <video controls autoPlay loop className="video-player-large">
                      <source src={`http://127.0.0.1:8000${result.video_path}`} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  ) : (
                    <div className="code-view-large">
                      <div className="code-view-header">
                        <span className="status-badge">
                          <div className={`status-dot ${result.syntax_valid ? 'valid' : 'invalid'}`}></div>
                          Syntax: {result.syntax_valid ? 'Valid' : 'Invalid'}
                        </span>
                      </div>
                      <pre>
                        {result.code || '# No code generated.'}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="media-footer">
              <span>This animation took 1 Generation Step and was processed successfully.</span>
              <div className="watermark">Made with Animind AI</div>
            </div>
          </div>
        </main>
      )}
    </div>
  );
}

export default App;
