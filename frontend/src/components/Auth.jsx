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
    
    // Check if Supabase URL is placeholder or missing
    const isSupabaseConfigured = import.meta.env.VITE_SUPABASE_URL && !import.meta.env.VITE_SUPABASE_URL.includes('placeholder')

    if (!isSupabaseConfigured) {
      // Automatic Local Guest Auth Session
      localStorage.setItem('lot_ai_user', JSON.stringify({ email: email || 'guest@lotai.dev', id: 'user_' + Date.now() }))
      window.location.reload()
      return
    }

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
      if (error.message?.includes('Failed to fetch')) {
        // Fallback to local session on network error
        localStorage.setItem('lot_ai_user', JSON.stringify({ email: email || 'user@lotai.dev', id: 'user_' + Date.now() }))
        window.location.reload()
        return
      }
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
      const errText = error.message || ''
      if (errText.includes('provider is not enabled') || errText.includes('validation_failed')) {
        setMessage({
          text: 'Google Sign-In is not enabled in your Supabase Project yet. Go to Supabase Dashboard -> Authentication -> Providers -> Enable Google.',
          type: 'error'
        })
      } else {
        setMessage({ text: error.message, type: 'error' })
      }
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
      const errText = error.message || ''
      if (errText.includes('provider is not enabled') || errText.includes('validation_failed')) {
        setMessage({
          text: 'GitHub Sign-In is not enabled in your Supabase Project yet. Go to Supabase Dashboard -> Authentication -> Providers -> Enable GitHub.',
          type: 'error'
        })
      } else {
        setMessage({ text: error.message, type: 'error' })
      }
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
          <p style={{ color: '#888', margin: 0, fontSize: '0.9rem' }}>{isLoginMode ? 'Enter your details to access LOT AI.' : 'Start building with LOT AI today.'}</p>
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
