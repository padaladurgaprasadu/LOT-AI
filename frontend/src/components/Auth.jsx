import { useState } from 'react'
import { supabase } from '../lib/supabaseClient'

export default function Auth() {
  const [loading, setLoading] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState({ text: '', type: '' })
  const [isLoginMode, setIsLoginMode] = useState(true)

  const handleAuth = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ text: '', type: '' })
    
    try {
      if (isLoginMode) {
        const { error } = await supabase.auth.signInWithPassword({ email, password })
        if (error) throw error
      } else {
        const { error } = await supabase.auth.signUp({ email, password })
        if (error) throw error
        setMessage({ text: 'Success! Check your email for a confirmation link.', type: 'success' })
      }
    } catch (error) {
      setMessage({ text: error.message, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const handleGoogleSignIn = async () => {
    setLoading(true)
    setMessage({ text: '', type: '' })
    try {
      const { error } = await supabase.auth.signInWithOAuth({ provider: 'google' })
      if (error) throw error
    } catch (error) {
      setMessage({ text: error.message, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const handleGithubSignIn = async () => {
    setLoading(true)
    setMessage({ text: '', type: '' })
    try {
      const { error } = await supabase.auth.signInWithOAuth({ provider: 'github' })
      if (error) throw error
    } catch (error) {
      setMessage({ text: error.message, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#0a0a0a', backgroundImage: 'radial-gradient(circle at 50% -20%, #1a1a2e, #0a0a0a 60%)' }}>
      <div style={{ width: '100%', maxWidth: '480px', padding: '30px', backgroundColor: '#111', borderRadius: '16px', border: '1px solid #333', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)' }}>
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '5px' }}>⚡</div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: '600', color: '#fff', margin: '0 0 5px 0' }}>{isLoginMode ? 'Welcome back' : 'Create an account'}</h2>
          <p style={{ color: '#888', margin: 0, fontSize: '0.9rem' }}>{isLoginMode ? 'Enter your details to access PrismAI.' : 'Start building with PrismAI today.'}</p>
        </div>
        
        <form onSubmit={handleAuth} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#aaa', marginBottom: '6px', fontWeight: '500' }}>Email Address</label>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{ width: '100%', padding: '12px 14px', borderRadius: '10px', border: '1px solid #333', backgroundColor: '#1a1a1a', color: '#fff', fontSize: '1rem', transition: 'border-color 0.2s', outline: 'none', boxSizing: 'border-box' }}
              onFocus={(e) => e.target.style.borderColor = 'var(--accent)'}
              onBlur={(e) => e.target.style.borderColor = '#333'}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#aaa', marginBottom: '6px', fontWeight: '500' }}>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ width: '100%', padding: '12px 14px', borderRadius: '10px', border: '1px solid #333', backgroundColor: '#1a1a1a', color: '#fff', fontSize: '1rem', transition: 'border-color 0.2s', outline: 'none', boxSizing: 'border-box' }}
              onFocus={(e) => e.target.style.borderColor = 'var(--accent)'}
              onBlur={(e) => e.target.style.borderColor = '#333'}
            />
          </div>
          
          {message.text && (
            <div style={{ padding: '12px 16px', borderRadius: '8px', backgroundColor: message.type === 'error' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)', color: message.type === 'error' ? '#ef4444' : '#10b981', fontSize: '0.9rem', border: `1px solid ${message.type === 'error' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)'}`, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>{message.type === 'error' ? '⚠️' : '✅'}</span>
              <span>{message.text}</span>
            </div>
          )}

          <button type="submit" disabled={loading} style={{ width: '100%', padding: '14px', borderRadius: '10px', backgroundColor: 'var(--accent)', color: '#fff', fontWeight: '600', fontSize: '1rem', border: 'none', cursor: loading ? 'not-allowed' : 'pointer', transition: 'opacity 0.2s, transform 0.1s', opacity: loading ? 0.7 : 1, marginTop: '10px' }}
            onMouseDown={(e) => !loading && (e.target.style.transform = 'scale(0.98)')}
            onMouseUp={(e) => e.target.style.transform = 'scale(1)'}
            onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
          >
            {loading ? <span className="spinner" style={{ width: '20px', height: '20px', display: 'inline-block', verticalAlign: 'middle' }}></span> : (isLoginMode ? 'Sign In' : 'Sign Up')}
          </button>
        </form>

        <div style={{ display: 'flex', alignItems: 'center', margin: '24px 0', color: '#666', fontSize: '0.85rem', fontWeight: '500' }}>
          <div style={{ flex: 1, height: '1px', backgroundColor: '#333' }}></div>
          <span style={{ padding: '0 12px' }}>OR</span>
          <div style={{ flex: 1, height: '1px', backgroundColor: '#333' }}></div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <button 
            onClick={handleGoogleSignIn}
            disabled={loading}
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', width: '100%', padding: '12px', borderRadius: '10px', backgroundColor: '#fff', color: '#000', fontWeight: '600', fontSize: '0.95rem', border: 'none', cursor: loading ? 'not-allowed' : 'pointer', transition: 'opacity 0.2s', opacity: loading ? 0.7 : 1 }}
          >
            <svg viewBox="0 0 24 24" width="20" height="20" xmlns="http://www.w3.org/2000/svg">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            Continue with Google
          </button>
          
          <button 
            onClick={handleGithubSignIn}
            disabled={loading}
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', width: '100%', padding: '12px', borderRadius: '10px', backgroundColor: '#24292e', color: '#fff', fontWeight: '600', fontSize: '0.95rem', border: '1px solid #333', cursor: loading ? 'not-allowed' : 'pointer', transition: 'opacity 0.2s', opacity: loading ? 0.7 : 1 }}
          >
            <svg viewBox="0 0 24 24" width="20" height="20" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" fill="#fff"/>
            </svg>
            Continue with GitHub
          </button>
        </div>

        <div style={{ textAlign: 'center', marginTop: '24px', fontSize: '0.9rem', color: '#888' }}>
          {isLoginMode ? "Don't have an account? " : "Already have an account? "}
          <button 
            onClick={() => { setIsLoginMode(!isLoginMode); setMessage({text: '', type: ''}); }} 
            style={{ background: 'none', border: 'none', color: 'var(--accent)', fontWeight: '600', cursor: 'pointer', padding: 0 }}
          >
            {isLoginMode ? 'Sign up' : 'Log in'}
          </button>
        </div>
      </div>
    </div>
  )
}
