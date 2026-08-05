import React, { useState, useEffect, useRef } from 'react';

const MODELS = [
  {
    id: 'sovereign-ultra',
    name: 'LOT Sovereign Ultra',
    description: 'Flagship model',
    context: '1M',
    speed: 'Medium',
    color: '#38bdf8',
    benchmarks: {
      coding: '92.4%',
      reasoning: '89.1%',
      math: '94.5%',
      speed: '45',
      multimodal: 'Yes',
      agentic: 'Yes'
    }
  },
  {
    id: 'prometheus-550b',
    name: 'LOT Prometheus 550B',
    description: 'Reasoning beast',
    context: '200K',
    speed: 'Slow',
    color: '#a855f7',
    benchmarks: {
      coding: '88.3%',
      reasoning: '93.2%',
      math: '91.8%',
      speed: '25',
      multimodal: 'Yes',
      agentic: 'Yes'
    }
  },
  {
    id: 'nemotron-flash',
    name: 'LOT Nemotron Flash',
    description: 'Fast daily coding',
    context: '200K',
    speed: 'Fast',
    color: '#22c55e',
    benchmarks: {
      coding: '85.6%',
      reasoning: '84.0%',
      math: '86.5%',
      speed: '120',
      multimodal: 'No',
      agentic: 'Yes'
    }
  },
  {
    id: 'architect-70b',
    name: 'LOT Architect 70B',
    description: 'Code architecture',
    context: '128K',
    speed: 'Medium',
    color: '#f59e0b',
    benchmarks: {
      coding: '87.9%',
      reasoning: '82.5%',
      math: '83.2%',
      speed: '65',
      multimodal: 'No',
      agentic: 'No'
    }
  },
  {
    id: 'haiku-lite',
    name: 'LOT Haiku Lite',
    description: 'Lightweight tasks',
    context: '64K',
    speed: 'Fast',
    color: '#ec4899',
    benchmarks: {
      coding: '75.2%',
      reasoning: '76.8%',
      math: '72.1%',
      speed: '180',
      multimodal: 'Yes',
      agentic: 'No'
    }
  }
];

const INITIAL_SESSIONS = [
  { id: '1', title: 'React Component Optimization', timestamp: '10:42 AM' },
  { id: '2', title: 'Database Schema Design', timestamp: 'Yesterday' },
  { id: '3', title: 'Explain Quantum Computing', timestamp: 'Mon, 2:15 PM' }
];

export default function LOTModelArena({ API_URL }) {
  const [selectedModel, setSelectedModel] = useState(MODELS[0]);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [tokensUsed, setTokensUsed] = useState(15000);
  const [sessions, setSessions] = useState(INITIAL_SESSIONS);
  const [activeSession, setActiveSession] = useState(INITIAL_SESSIONS[0].id);
  
  const messagesEndRef = useRef(null);

  const maxTokens = parseInt(selectedModel.context.replace('K', '000').replace('1M', '1000000'), 10);
  const tokenPercentage = (tokensUsed / maxTokens) * 100;

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isTyping]);

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);
    setTokensUsed((prev) => prev + inputValue.length * 2);

    setTimeout(() => {
      const botMessage = {
        role: 'assistant',
        content: `I am ${selectedModel.name}. Here is a simulated response to: "${userMessage.content}". My context is ${selectedModel.context} and I am optimized for your tasks.`
      };
      setMessages((prev) => [...prev, botMessage]);
      setIsTyping(false);
      setTokensUsed((prev) => prev + botMessage.content.length * 2);
    }, 1200);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div style={styles.container}>
      {/* Sidebar */}
      <div style={styles.sidebar}>
        <div style={styles.sidebarHeader}>
          <h2 style={styles.brandTitle}>LOT Arena</h2>
          <button style={styles.newChatBtn} onClick={() => {
            const newId = Date.now().toString();
            setSessions([{id: newId, title: 'New Conversation', timestamp: 'Just now'}, ...sessions]);
            setActiveSession(newId);
            setMessages([]);
            setTokensUsed(0);
          }}>
            + New Chat
          </button>
        </div>
        <div style={styles.sessionList}>
          {sessions.map(s => (
            <div 
              key={s.id} 
              style={{...styles.sessionItem, ...(activeSession === s.id ? styles.activeSession : {})}}
              onClick={() => setActiveSession(s.id)}
            >
              <div style={styles.sessionTitle}>{s.title}</div>
              <div style={styles.sessionTime}>{s.timestamp}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div style={styles.main}>
        {/* Model Selector */}
        <div style={styles.modelSelectorContainer}>
          <div style={styles.modelSelectorBar}>
            {MODELS.map(model => (
              <div 
                key={model.id}
                style={{
                  ...styles.modelCard, 
                  borderColor: selectedModel.id === model.id ? model.color : '#1e293b',
                  backgroundColor: selectedModel.id === model.id ? '#13151c' : 'transparent'
                }}
                onClick={() => setSelectedModel(model)}
              >
                <div style={styles.modelCardHeader}>
                  <div style={{...styles.modelColorBadge, backgroundColor: model.color}} />
                  <span style={styles.modelName}>{model.name}</span>
                </div>
                <div style={styles.modelCardStats}>
                  <span>{model.context} ctx</span>
                  <span style={{color: '#64748b'}}>•</span>
                  <span>{model.speed}</span>
                </div>
              </div>
            ))}
          </div>
          
          {/* Token Counter */}
          <div style={styles.tokenCounterContainer}>
            <div style={styles.tokenBarBg}>
              <div style={{...styles.tokenBarFill, width: `${Math.min(tokenPercentage, 100)}%`, backgroundColor: selectedModel.color}} />
            </div>
            <div style={styles.tokenCounterStats}>
              <span>{tokensUsed.toLocaleString()} / {maxTokens.toLocaleString()} tokens</span>
              {tokenPercentage > 80 && (
                <span style={styles.fallbackBadge}>Auto-fallback to LOT Nemotron Flash</span>
              )}
            </div>
          </div>
        </div>

        {/* Benchmark Table */}
        <div style={styles.benchmarkContainer}>
          <h3 style={styles.sectionTitle}>Model Benchmarks</h3>
          <div style={styles.tableWrapper}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>Model</th>
                  <th style={styles.th}>SWE-bench</th>
                  <th style={styles.th}>GPQA</th>
                  <th style={styles.th}>MATH-500</th>
                  <th style={styles.th}>Ctx</th>
                  <th style={styles.th}>Speed (t/s)</th>
                  <th style={styles.th}>Vision</th>
                  <th style={styles.th}>Agentic</th>
                </tr>
              </thead>
              <tbody>
                {MODELS.map(model => (
                  <tr key={model.id} style={{backgroundColor: selectedModel.id === model.id ? '#13151c' : 'transparent'}}>
                    <td style={{...styles.td, color: model.color, fontWeight: 'bold'}}>{model.name}</td>
                    <td style={styles.td}>{model.benchmarks.coding}</td>
                    <td style={styles.td}>{model.benchmarks.reasoning}</td>
                    <td style={styles.td}>{model.benchmarks.math}</td>
                    <td style={styles.td}>{model.context}</td>
                    <td style={styles.td}>{model.benchmarks.speed}</td>
                    <td style={styles.td}>{model.benchmarks.multimodal}</td>
                    <td style={styles.td}>{model.benchmarks.agentic}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Chat Area */}
        <div style={styles.chatContainer}>
          <div style={styles.messagesList}>
            {messages.length === 0 && (
              <div style={styles.emptyState}>
                Send a message to start chatting with {selectedModel.name}
              </div>
            )}
            {messages.map((msg, idx) => (
              <div key={idx} style={{...styles.messageRow, justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'}}>
                <div style={{
                  ...styles.messageBubble,
                  backgroundColor: msg.role === 'user' ? '#1e293b' : '#13151c',
                  border: msg.role === 'user' ? 'none' : `1px solid ${selectedModel.color}40`
                }}>
                  {msg.content}
                </div>
              </div>
            ))}
            {isTyping && (
              <div style={{...styles.messageRow, justifyContent: 'flex-start'}}>
                <div style={{...styles.messageBubble, backgroundColor: '#13151c', border: `1px solid ${selectedModel.color}40`}}>
                  <div style={styles.typingIndicator} />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div style={styles.inputArea}>
            <textarea
              style={styles.textarea}
              placeholder={`Message ${selectedModel.name}...`}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={2}
            />
            <button style={{...styles.sendBtn, backgroundColor: selectedModel.color}} onClick={handleSendMessage}>
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    height: '100vh',
    width: '100%',
    backgroundColor: '#0b0c10',
    color: '#f8fafc',
    fontFamily: 'Inter, system-ui, sans-serif',
    overflow: 'hidden'
  },
  sidebar: {
    width: '260px',
    backgroundColor: '#0b0c10',
    borderRight: '1px solid #1e293b',
    display: 'flex',
    flexDirection: 'column',
  },
  sidebarHeader: {
    padding: '20px',
    borderBottom: '1px solid #1e293b'
  },
  brandTitle: {
    margin: '0 0 16px 0',
    fontSize: '20px',
    fontWeight: '600'
  },
  newChatBtn: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#1e293b',
    color: '#f8fafc',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: '500',
    transition: 'background-color 0.2s ease',
  },
  sessionList: {
    flex: 1,
    overflowY: 'auto',
    padding: '12px'
  },
  sessionItem: {
    padding: '12px',
    borderRadius: '8px',
    cursor: 'pointer',
    marginBottom: '8px',
    transition: 'background-color 0.2s ease'
  },
  activeSession: {
    backgroundColor: '#13151c',
    border: '1px solid #1e293b'
  },
  sessionTitle: {
    fontSize: '14px',
    fontWeight: '500',
    marginBottom: '4px',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis'
  },
  sessionTime: {
    fontSize: '12px',
    color: '#64748b'
  },
  main: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden'
  },
  modelSelectorContainer: {
    padding: '20px',
    borderBottom: '1px solid #1e293b',
    backgroundColor: '#0b0c10'
  },
  modelSelectorBar: {
    display: 'flex',
    gap: '12px',
    overflowX: 'auto',
    paddingBottom: '8px',
    scrollbarWidth: 'none',
  },
  modelCard: {
    minWidth: '200px',
    padding: '12px',
    borderRadius: '12px',
    border: '1px solid #1e293b',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  },
  modelCardHeader: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '8px'
  },
  modelColorBadge: {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    marginRight: '8px'
  },
  modelName: {
    fontSize: '14px',
    fontWeight: '600'
  },
  modelCardStats: {
    fontSize: '12px',
    color: '#94a3b8',
    display: 'flex',
    gap: '8px'
  },
  tokenCounterContainer: {
    marginTop: '16px'
  },
  tokenBarBg: {
    height: '4px',
    backgroundColor: '#1e293b',
    borderRadius: '2px',
    overflow: 'hidden'
  },
  tokenBarFill: {
    height: '100%',
    transition: 'width 0.3s ease, background-color 0.3s ease'
  },
  tokenCounterStats: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontSize: '12px',
    color: '#64748b',
    marginTop: '6px'
  },
  fallbackBadge: {
    backgroundColor: '#f59e0b20',
    color: '#f59e0b',
    padding: '2px 8px',
    borderRadius: '10px',
    fontSize: '11px',
    fontWeight: '500'
  },
  benchmarkContainer: {
    padding: '20px',
    borderBottom: '1px solid #1e293b'
  },
  sectionTitle: {
    margin: '0 0 12px 0',
    fontSize: '14px',
    fontWeight: '600',
    color: '#94a3b8'
  },
  tableWrapper: {
    overflowX: 'auto'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '13px'
  },
  th: {
    textAlign: 'left',
    padding: '8px 12px',
    color: '#64748b',
    borderBottom: '1px solid #1e293b',
    fontWeight: '500'
  },
  td: {
    padding: '10px 12px',
    borderBottom: '1px solid #1e293b'
  },
  chatContainer: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#0b0c10',
    overflow: 'hidden'
  },
  messagesList: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px'
  },
  emptyState: {
    margin: 'auto',
    color: '#64748b',
    fontSize: '14px'
  },
  messageRow: {
    display: 'flex',
    width: '100%'
  },
  messageBubble: {
    maxWidth: '70%',
    padding: '12px 16px',
    borderRadius: '12px',
    fontSize: '14px',
    lineHeight: '1.5'
  },
  typingIndicator: {
    width: '8px',
    height: '8px',
    backgroundColor: '#94a3b8',
    borderRadius: '50%',
    animation: 'pulse 1.5s infinite ease-in-out'
  },
  inputArea: {
    padding: '20px',
    borderTop: '1px solid #1e293b',
    display: 'flex',
    gap: '12px',
    backgroundColor: '#0b0c10'
  },
  textarea: {
    flex: 1,
    backgroundColor: '#13151c',
    border: '1px solid #1e293b',
    borderRadius: '8px',
    padding: '12px',
    color: '#f8fafc',
    fontFamily: 'inherit',
    fontSize: '14px',
    resize: 'none',
    outline: 'none',
  },
  sendBtn: {
    padding: '0 20px',
    color: '#0b0c10',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: '600',
    fontSize: '14px',
    transition: 'opacity 0.2s ease'
  }
};
