import React, { useState, useRef, useEffect } from 'react';

/**
 * LOT AI v1.0 (Prometheus) — Fully Mobile-Responsive Matte Pill Input Bar
 * Inspired by ChatGPT pill container, customized for LOT AI with NO glowing effects.
 * 
 * Mobile Enhancements:
 * - 16px font size on mobile screens to prevent iOS Safari auto-zoom
 * - Dynamic responsive layout for mobile, tablet, and desktop viewports
 * - Icon-only search badge on small screens (< 480px)
 * - Touch-optimized 36px-40px button targets
 * - Scrollable responsive slash menu popup
 * - 100% full-width mobile container with safe padding
 */
export default function LOTAIInputBar({
  value,
  onChange,
  onSubmit,
  onImageUpload,
  selectedImages = [],
  onRemoveImage,
  isRecording = false,
  onToggleVoice,
  isWebSearchEnabled = false,
  onToggleWebSearch,
  isLoading = false,
  placeholder = "Ask LOT AI Prometheus..."
}) {
  const [showSlashMenu, setShowSlashMenu] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  // Detect screen size for responsive adjustments
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 640);
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const slashCommands = [
    { cmd: '/interview-me', desc: 'Ask strategic questions before building' },
    { cmd: '/plan', desc: 'Generate C4 blueprint & task breakdown' },
    { cmd: '/build', desc: 'Execute autonomous code generation' },
    { cmd: '/test', desc: 'Run automated verification & self-healing' },
    { cmd: '/ship', desc: 'Package and deploy 3D WebGL preview' },
    { cmd: '/hermes', desc: 'Execute Hermes 8-section creative super-intelligence' },
    { cmd: '/fable', desc: 'Generate 5-phase longform creative narrative' },
    { cmd: '/mythos', desc: 'Synthesize world pantheon & creation lore' },
    { cmd: '/agent-skills', desc: 'View 24 Production Engineering Skills' },
  ];

  // Handle slash key input
  const handleInputChange = (e) => {
    const val = e.target.value;
    onChange(val);
    if (val.startsWith('/') && !val.includes(' ')) {
      setShowSlashMenu(true);
    } else {
      setShowSlashMenu(false);
    }
  };

  const selectSlashCommand = (cmd) => {
    onChange(`${cmd} `);
    setShowSlashMenu(false);
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !isLoading) {
        onSubmit(e);
      }
    }
  };

  return (
    <div className="lotai-input-wrapper" style={{
      width: '100%',
      maxWidth: '840px',
      margin: '0 auto',
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: isMobile ? '0 4px' : '0 8px'
    }}>
      
      {/* RESPONSIVE SLASH COMMAND MENU POPUP */}
      {showSlashMenu && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          marginBottom: '8px',
          left: isMobile ? '8px' : '16px',
          right: isMobile ? '8px' : '16px',
          maxHeight: '220px',
          overflowY: 'auto',
          backgroundColor: '#18181c',
          border: '1px solid #2e2e38',
          borderRadius: '16px',
          padding: '6px',
          zIndex: 100,
          boxShadow: 'none', // Strictly no glow
          display: 'flex',
          flexDirection: 'column',
          gap: '2px'
        }}>
          <div style={{ padding: '6px 10px', fontSize: '0.7rem', fontWeight: '600', color: '#a1a1aa', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            LOT AI Prometheus Commands
          </div>
          {slashCommands.map((item) => (
            <button
              key={item.cmd}
              type="button"
              onClick={() => selectSlashCommand(item.cmd)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: isMobile ? '8px 10px' : '10px 14px',
                backgroundColor: 'transparent',
                border: 'none',
                borderRadius: '10px',
                color: '#f4f4f5',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'background-color 0.15s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#27272a'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
            >
              <span style={{ fontWeight: '600', color: '#38bdf8', fontFamily: 'monospace', fontSize: isMobile ? '0.85rem' : '0.9rem' }}>{item.cmd}</span>
              {!isMobile && <span style={{ fontSize: '0.78rem', color: '#a1a1aa' }}>{item.desc}</span>}
            </button>
          ))}
        </div>
      )}

      {/* ATTACHED IMAGE PREVIEWS */}
      {selectedImages.length > 0 && (
        <div style={{
          width: '100%',
          display: 'flex',
          gap: '8px',
          padding: '6px 12px',
          overflowX: 'auto',
          marginBottom: '6px'
        }}>
          {selectedImages.map((img, idx) => (
            <div key={idx} style={{ position: 'relative', display: 'inline-block', flexShrink: 0 }}>
              <img src={img} alt={`Attachment ${idx}`} style={{ height: '48px', width: '48px', borderRadius: '10px', objectFit: 'cover', border: '1px solid #3f3f46' }} />
              <button
                type="button"
                onClick={() => onRemoveImage && onRemoveImage(idx)}
                style={{
                  position: 'absolute',
                  top: '-5px',
                  right: '-5px',
                  backgroundColor: '#ef4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '50%',
                  width: '18px',
                  height: '18px',
                  fontSize: '11px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}

      {/* MAIN MOBILE-RESPONSIVE MATTE PILL INPUT BAR */}
      <form
        onSubmit={onSubmit}
        style={{
          width: '100%',
          backgroundColor: '#18181b',
          borderRadius: '9999px',     // Perfect pill capsule
          padding: isMobile ? '4px 6px 4px 10px' : '6px 8px 6px 16px',
          display: 'flex',
          alignItems: 'center',
          gap: isMobile ? '6px' : '10px',
          border: '1px solid #27272a', // Clean matte border, NO GLOW
          boxShadow: 'none',          // Explicitly no glowing effects
          transition: 'border-color 0.2s ease, background-color 0.2s ease'
        }}
      >
        {/* FILE INPUT (HIDDEN) */}
        <input
          type="file"
          multiple
          accept="image/*"
          ref={fileInputRef}
          onChange={onImageUpload}
          style={{ display: 'none' }}
        />

        {/* LEFT (+) ATTACHMENT BUTTON */}
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          style={{
            width: isMobile ? '32px' : '36px',
            height: isMobile ? '32px' : '36px',
            borderRadius: '50%',
            backgroundColor: '#27272a',
            border: 'none',
            color: '#e4e4e7',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
            transition: 'background-color 0.15s ease'
          }}
          title="Attach files or images"
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#3f3f46'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#27272a'}
        >
          <svg width={isMobile ? "16" : "18"} height={isMobile ? "16" : "18"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>

        {/* INPUT TEXTAREA */}
        <input
          ref={textareaRef}
          type="text"
          value={value}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder={isMobile ? "Ask LOT AI..." : placeholder}
          disabled={isLoading}
          style={{
            flex: 1,
            minWidth: 0,
            backgroundColor: 'transparent',
            border: 'none',
            outline: 'none',
            color: '#f4f4f5',
            fontSize: isMobile ? '16px' : '0.98rem', // 16px on mobile prevents iOS Safari auto-zoom!
            fontFamily: 'inherit',
            fontWeight: '400',
            padding: isMobile ? '6px 2px' : '8px 4px',
            boxShadow: 'none'
          }}
        />

        {/* WEB SEARCH TOGGLE BUTTON (RESPONSIVE BADGE) */}
        {onToggleWebSearch && (
          <button
            type="button"
            onClick={onToggleWebSearch}
            style={{
              backgroundColor: isWebSearchEnabled ? '#27272a' : 'transparent',
              border: isWebSearchEnabled ? '1px solid #3f3f46' : 'none',
              borderRadius: '20px',
              padding: isMobile ? '5px 8px' : '6px 10px',
              color: isWebSearchEnabled ? '#38bdf8' : '#71717a',
              fontSize: '0.8rem',
              fontWeight: '500',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              flexShrink: 0,
              transition: 'all 0.15s ease'
            }}
            title={isWebSearchEnabled ? "Web Search Active" : "Enable Web Search"}
          >
            <svg width={isMobile ? "13" : "14"} height={isMobile ? "13" : "14"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="2" y1="12" x2="22" y2="12"></line>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            </svg>
            {!isMobile && <span style={{ fontSize: '0.75rem' }}>Search</span>}
          </button>
        )}

        {/* MICROPHONE VOICE BUTTON */}
        <button
          type="button"
          onClick={onToggleVoice}
          style={{
            width: isMobile ? '32px' : '36px',
            height: isMobile ? '32px' : '36px',
            borderRadius: '50%',
            backgroundColor: isRecording ? '#ef4444' : 'transparent',
            border: 'none',
            color: isRecording ? '#ffffff' : '#9ca3af',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
            transition: 'background-color 0.15s ease, color 0.15s ease'
          }}
          title={isRecording ? "Stop Recording" : "Voice Input"}
        >
          <svg width={isMobile ? "16" : "18"} height={isMobile ? "16" : "18"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="10" y1="23" x2="14" y2="23"></line>
          </svg>
        </button>

        {/* RIGHTMOST SOLID CIRCULAR ACTION BUTTON */}
        <button
          type="submit"
          disabled={isLoading || !value.trim()}
          style={{
            width: isMobile ? '34px' : '40px',
            height: isMobile ? '34px' : '40px',
            borderRadius: '50%',
            backgroundColor: (isLoading || !value.trim()) ? '#27272a' : '#ffffff', // Solid white pill button when ready!
            border: 'none',
            color: (isLoading || !value.trim()) ? '#71717a' : '#000000',           // Crisp black icon on white background!
            cursor: (isLoading || !value.trim()) ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
            transition: 'transform 0.15s ease, background-color 0.15s ease',
            boxShadow: 'none'
          }}
          title={value.trim() ? "Send Message" : "Audio / Send"}
        >
          {value.trim() ? (
            /* Send Up Arrow Icon */
            <svg width={isMobile ? "16" : "18"} height={isMobile ? "16" : "18"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="19" x2="12" y2="5"></line>
              <polyline points="5 12 12 5 19 12"></polyline>
            </svg>
          ) : (
            /* Audio Waveform Bars Icon */
            <svg width={isMobile ? "16" : "18"} height={isMobile ? "16" : "18"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="6" y1="10" x2="6" y2="14"></line>
              <line x1="10" y1="6" x2="10" y2="18"></line>
              <line x1="14" y1="8" x2="14" y2="16"></line>
              <line x1="18" y1="11" x2="18" y2="13"></line>
            </svg>
          )}
        </button>
      </form>
    </div>
  );
}
