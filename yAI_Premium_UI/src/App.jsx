import { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'agent',
      agentName: 'System Core',
      content: 'yAI Operating System initialized. I am ready to construct your architecture. What are we building today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [previewUrl, setPreviewUrl] = useState('');
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMsg = { id: Date.now(), role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsProcessing(true);

    // Simulate yAI Engine process (Router -> Planner -> Developer -> Executer)
    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'agent',
        agentName: 'Router Agent',
        content: 'Analyzing request. Delegating to architectural and engineering teams...'
      }]);
    }, 1000);

    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: Date.now() + 2,
        role: 'agent',
        agentName: 'Full Stack Developer',
        content: 'Drafting application logic based on the blueprint. Compiling React components and API routes.'
      }]);
    }, 2500);

    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: Date.now() + 3,
        role: 'agent',
        agentName: 'Executer Agent',
        content: 'Code verified by Reviewer. Sandboxing application. Starting Live Preview Server on port 8080.'
      }]);
      // Set the mock preview URL
      setPreviewUrl('http://localhost:8080');
      setIsProcessing(false);
    }, 4500);
  };

  return (
    <div className="app-container">
      
      {/* LEFT PANEL: Chat & Thought Stream */}
      <div className="glass-panel chat-panel animate-slide-up">
        <div className="panel-header">
          <div className="logo-container">
            <h1>yAI OS</h1>
          </div>
          <div className="status-indicator">
            <div className={`status-dot ${!isProcessing ? 'idle' : ''}`}></div>
            {isProcessing ? 'Processing' : 'Online'}
          </div>
        </div>

        <div className="chat-history">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.role}`}>
              {msg.role === 'agent' ? (
                <>
                  <div className="agent-header">
                    <div className="agent-avatar">{msg.agentName.substring(0, 2).toUpperCase()}</div>
                    <span className="agent-name">{msg.agentName}</span>
                  </div>
                  <div className="agent-content">{msg.content}</div>
                </>
              ) : (
                msg.content
              )}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        <div className="chat-input-container">
          <form className="chat-input-wrapper" onSubmit={handleSend}>
            <input 
              type="text" 
              className="chat-input"
              placeholder="Command yAI to build something..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isProcessing}
            />
            <button type="submit" className="send-btn" disabled={isProcessing}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
        </div>
      </div>

      {/* RIGHT PANEL: Live Preview Engine */}
      <div className="glass-panel preview-panel animate-slide-up" style={{ animationDelay: '0.1s' }}>
        <div className="preview-header">
          <div className="browser-dots">
            <div className="browser-dot dot-r"></div>
            <div className="browser-dot dot-y"></div>
            <div className="browser-dot dot-g"></div>
          </div>
          <div className="url-bar">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span className="mono">{previewUrl || 'about:blank'}</span>
          </div>
        </div>
        
        <div className="preview-content">
          {previewUrl ? (
            <div style={{width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#f8f9fa'}}>
                {/* Normally this is an iframe, but for this preview simulation we render a mock */}
                <h1 style={{color: '#333'}}>Digital Clock App (Simulation)</h1>
                <p>Connected to <b>{previewUrl}</b></p>
                <div style={{marginTop: '20px', padding: '20px', background: '#111', color: '#0f0', fontFamily: 'monospace', fontSize: '2rem', borderRadius: '10px', boxShadow: '0 0 20px rgba(0,255,0,0.2)'}}>
                    14:32:05
                </div>
            </div>
            // <iframe src={previewUrl} className="preview-iframe" title="Live Preview" />
          ) : (
            <div className="empty-state">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ccc" strokeWidth="1">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                <line x1="8" y1="21" x2="16" y2="21"></line>
                <line x1="12" y1="17" x2="12" y2="21"></line>
              </svg>
              <p>Live Preview Engine Idle</p>
            </div>
          )}
        </div>
      </div>

    </div>
  );
}

export default App;
