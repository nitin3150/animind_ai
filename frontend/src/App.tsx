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

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content?: string;
  result?: GenerateResponse;
  error?: string;
  loading?: boolean;
}

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (endOfMessagesRef.current) {
      endOfMessagesRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const currentQuery = query;
    const isFirstPrompt = messages.length === 0;
    const endpoint = isFirstPrompt ? 'http://127.0.0.1:8000/generate/' : 'http://127.0.0.1:8000/generate/edit';

    const userMsgId = Date.now().toString() + '-user';
    const aiMsgId = Date.now().toString() + '-ai';

    setMessages(prev => [
      ...prev,
      { id: userMsgId, role: 'user', content: currentQuery },
      { id: aiMsgId, role: 'assistant', loading: true }
    ]);
    setQuery('');

    try {
      const { data } = await axios.post<GenerateResponse>(endpoint, {
        user_query: currentQuery
      });
      setMessages(prev => prev.map(msg =>
        msg.id === aiMsgId ? { ...msg, loading: false, result: data } : msg
      ));
    } catch (err: any) {
      console.error(err);
      const errorText = err.response?.data?.detail || 'Failed to connect to the Animind AI server.';
      setMessages(prev => prev.map(msg =>
        msg.id === aiMsgId ? { ...msg, loading: false, error: errorText } : msg
      ));
    }
  };

  const handleReset = () => {
    setQuery('');
    setMessages([]);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  const isSplitView = messages.length > 0;
  
  const currentAiMessage = messages.length > 0 ? messages[messages.length - 1] : null;
  const isCurrentlyLoading = currentAiMessage?.role === 'assistant' && currentAiMessage?.loading;
  const latestAiMessageWithResult = [...messages].reverse().find(m => m.role === 'assistant' && m.result);
  const resultToDisplay = latestAiMessageWithResult?.result;
  const errorToDisplay = currentAiMessage?.role === 'assistant' && currentAiMessage?.error ? currentAiMessage.error : null;

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
                disabled={isCurrentlyLoading}
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
                    disabled={isCurrentlyLoading || !query.trim()}
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
            <div className="chat-header" style={{ padding: '16px', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ margin: 0, fontSize: '14px', fontWeight: 600 }}>Chat History</h3>
              <button 
                onClick={handleReset}
                className="new-session-btn"
              >
                + New Session
              </button>
            </div>
            <div className="chat-messages" style={{ height: 'calc(100% - 130px)', overflowY: 'auto' }}>
              {messages.map((msg) => (
                <div key={msg.id}>
                  {msg.role === 'user' ? (
                    <div className="user-message">
                      {msg.content}
                    </div>
                  ) : (
                    <div className="ai-message">
                      <div className="ai-avatar-name">
                        <Sparkles size={16} color="var(--accent-color)" />
                        <span>Animind AI</span>
                      </div>
                      {msg.loading && (
                        <div className="loading-state">
                          <Activity size={20} className="spinner" />
                          <span>Crafting your mathematical animation...</span>
                        </div>
                      )}
                      {msg.error && (
                        <div className="error-message">
                          <AlertCircle size={20} />
                          <span>{msg.error}</span>
                        </div>
                      )}
                      {msg.result && !msg.loading && (
                        <div className="success-state">
                          <p>
                            Your animation is ready! The media player on the right shows the generated mathematical visualization.
                          </p>
                          <div className="code-fragment-btn">
                            <Code2 size={14} />
                            Generated Manim Script
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
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
                    disabled={isCurrentlyLoading}
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
                        disabled={isCurrentlyLoading || !query.trim()}
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
              {isCurrentlyLoading && !resultToDisplay && !errorToDisplay && (
                <div className="placeholder-media">
                  <Activity size={48} className="spinner" color="var(--accent-color)" />
                  <p>Compiling rendering engine...</p>
                </div>
              )}

              {!isCurrentlyLoading && !resultToDisplay && errorToDisplay && (
                <div className="placeholder-media error-media">
                  <AlertCircle size={48} color="#ef4444" />
                  <p>Failed to generate view.</p>
                </div>
              )}

              {resultToDisplay && (
                <div className="result-display" style={{ opacity: isCurrentlyLoading ? 0.6 : 1 }}>
                  {resultToDisplay.video_path ? (
                    <video key={resultToDisplay.video_path} controls autoPlay loop className="video-player-large">
                      <source src={`http://127.0.0.1:8000${resultToDisplay.video_path}`} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  ) : (
                    <div className="code-view-large">
                      <div className="code-view-header">
                        <span className="status-badge">
                          <div className={`status-dot ${resultToDisplay.syntax_valid ? 'valid' : 'invalid'}`}></div>
                          Syntax: {resultToDisplay.syntax_valid ? 'Valid' : 'Invalid'}
                        </span>
                      </div>
                      <pre>
                        {resultToDisplay.code || '# No code generated.'}
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
