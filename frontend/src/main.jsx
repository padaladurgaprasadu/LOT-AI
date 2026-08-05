import React, { StrictMode, Component } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("React Error Boundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '40px', color: '#f87171', background: '#09090b', minHeight: '100vh', fontFamily: 'sans-serif', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
          <h2 style={{ color: '#60a5fa', marginBottom: '16px' }}>⚡ LOT AI React Guard</h2>
          <p style={{ color: '#a1a1aa', marginBottom: '20px' }}>An error was caught during rendering. Click below to clear cache and load fresh workspace:</p>
          <pre style={{ background: '#18181b', padding: '16px', borderRadius: '8px', color: '#fca5a5', maxWidth: '600px', overflowX: 'auto', textAlign: 'left', marginBottom: '24px' }}>
            {this.state.error?.toString()}
          </pre>
          <button onClick={() => { localStorage.clear(); sessionStorage.clear(); window.location.reload(); }} style={{ padding: '12px 24px', background: '#0284c7', color: 'white', border: 'none', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer' }}>
            🔄 Reset & Reload Workspace
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
