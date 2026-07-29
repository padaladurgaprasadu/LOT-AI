import { useState, useEffect, useRef } from 'react'
import './App.css'
import prismaiLogo from './assets/prismai_logo.png'
import Auth from './components/Auth'
import Chat from './components/Chat'
import { supabase } from './lib/supabaseClient'
import ArchitectureViewer from './components/ArchitectureViewer'
import ArtifactViewer from './components/ArtifactViewer'
import ProgressDashboard from './components/ProgressDashboard'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkBreaks from 'remark-breaks'
import PlatformDashboards from './components/PlatformDashboards'
import AIWorkspaceTabs from './components/AIWorkspaceTabs'

const handleMarkdownClick = async (e) => {
  const target = e.target;
  if (target.classList.contains('copy-code-btn')) {
    const code = decodeURIComponent(target.getAttribute('data-code'));
    navigator.clipboard.writeText(code);
    target.innerText = 'Copied!';
    setTimeout(() => { target.innerText = 'Copy'; }, 2000);
  } else if (target.classList.contains('run-code-btn')) {
    const code = decodeURIComponent(target.getAttribute('data-code'));
    const lang = target.getAttribute('data-lang');
    const blockId = target.getAttribute('data-block-id');
    const outputDiv = document.getElementById(`sandbox-${blockId}`);
    
    if (!outputDiv) return;
    
    outputDiv.style.display = 'block';
    outputDiv.innerHTML = '<div style="padding: 12px; color: #888; font-family: monospace; font-size: 0.85rem;">Running...</div>';
    target.innerText = 'Running...';
    target.style.color = '#888';
    target.disabled = true;
    
    // Map languages for Piston API
    let pistonLang = lang;
    if (lang === 'js' || lang === 'node') pistonLang = 'javascript';
    if (lang === 'py') pistonLang = 'python';
    
    // Use VITE_API_URL or local fallback
    const apiUrl = import.meta.env.VITE_API_URL || window.location.origin;
    
    try {
      const res = await fetch(`${apiUrl}/api/run-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          language: pistonLang,
          code: btoa(unescape(encodeURIComponent(code))),
          is_base64: true
        })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || JSON.stringify(data) || "Execution API failed with status " + res.status);
      }
      const output = data.output || data.message || "No output returned.";
      outputDiv.innerHTML = `<pre style="margin:0; padding:12px; background:#050505; color:#4ade80; font-family:monospace; font-size:0.85rem; overflow-x:auto;">${output.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>`;
    } catch (err) {
      outputDiv.innerHTML = `<div style="padding: 12px; color: #ef4444; font-family: monospace; font-size: 0.85rem;">Error: ${err.message}</div>`;
    } finally {
      target.innerText = 'Run';
      target.style.color = '#4ade80';
      target.disabled = false;
    }
  }
};

const CodeBlock = ({ node, className, children, ...props }) => {
  const match = /language-(\w+)/.exec(className || '');
  const language = match ? match[1] : 'text';
  const text = String(children).replace(/\n$/, '');
  
  const isInline = !match && !text.includes('\n');
  
  if (isInline) {
    return <code style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px', fontFamily: 'monospace' }} className={className} {...props}>{children}</code>;
  }
  
  const encodedCode = encodeURIComponent(text);
  const blockId = Math.random().toString(36).substring(2, 9);
  
  const supportedRunLangs = ['python', 'py', 'javascript', 'js', 'node'];
  const runBtnHTML = supportedRunLangs.includes(language.toLowerCase()) 
    ? <button className="run-code-btn" data-code={encodedCode} data-lang={language} data-block-id={blockId} style={{background: 'none', border: 'none', color: '#4ade80', cursor: 'pointer', fontSize: '0.75rem', transition: 'color 0.2s'}} onMouseOver={(e)=>e.target.style.color='#fff'} onMouseOut={(e)=>e.target.style.color='#4ade80'}>Run</button>
    : null;
    
  return (
    <div className="code-block-wrapper" style={{ position: 'relative', margin: '1em 0', borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--border-color)' }}>
      <div style={{ background: '#1e1e1e', padding: '6px 12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', color: '#888', fontSize: '0.75rem', fontFamily: 'monospace' }}>
        <span>{language}</span>
        <div style={{ display: 'flex', gap: '16px' }}>
          {runBtnHTML}
          <button className="copy-code-btn" data-code={encodedCode} style={{ background: 'none', border: 'none', color: '#aaa', cursor: 'pointer', fontSize: '0.75rem', transition: 'color 0.2s' }} onMouseOver={(e)=>e.target.style.color='#fff'} onMouseOut={(e)=>e.target.style.color='#aaa'}>Copy</button>
        </div>
      </div>
      <pre style={{ margin: 0, borderRadius: 0, padding: '16px', background: '#0d0d0d', overflowX: 'auto' }}>
        <code className={className} {...props}>{children}</code>
      </pre>
      <div id={`sandbox-${blockId}`} style={{ display: 'none', borderTop: '1px dashed var(--border-color)', background: '#050505' }}></div>
    </div>
  );
};

const ImageBlock = ({ node, ...props }) => {
  const [hasError, setHasError] = useState(false);
  if (hasError || !props.src) return null;

  return (
    <div style={{ margin: '16px 0', display: 'flex', justifyContent: 'center', width: '100%' }}>
      <img 
        {...props} 
        referrerPolicy="no-referrer"
        onError={() => setHasError(true)} 
        style={{ 
          width: '100%', 
          maxHeight: '450px', 
          borderRadius: '16px', 
          border: '1px solid rgba(255, 255, 255, 0.15)', 
          boxShadow: '0 12px 30px rgba(0,0,0,0.6)', 
          objectFit: 'cover',
          display: 'block'
        }} 
      />
    </div>
  );
};

const renderMessageContent = (content, onOpenArchitecture) => {
  if (!content.includes('<architecture>')) {
      return (
          <div className="markdown-body" onClick={handleMarkdownClick}>
              <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]} components={{ code: CodeBlock, img: ImageBlock }}>
                  {content}
              </ReactMarkdown>
          </div>
      );
  }
  
  const parts = cleanContent.split(/(<architecture>[\s\S]*?(?:<\/architecture>|$))/);
  return parts.map((part, i) => {
      if (part.startsWith('<architecture>')) {
          if (part.endsWith('</architecture>')) {
              let jsonStr = part.replace('<architecture>', '').replace('</architecture>', '').replace(/```json/g, '').replace(/```/g, '').trim();
              const startIdx = jsonStr.indexOf('{');
              const endIdx = jsonStr.lastIndexOf('}');
              if (startIdx !== -1 && endIdx !== -1) jsonStr = jsonStr.substring(startIdx, endIdx + 1);
              return (
                <div key={i} style={{ margin: '16px 0' }}>
                  <button 
                    onClick={() => onOpenArchitecture(jsonStr)}
                    style={{
                      background: 'linear-gradient(135deg, #3b82f6, #2563eb)',
                      color: 'white',
                      border: 'none',
                      padding: '12px 24px',
                      borderRadius: '8px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      boxShadow: '0 4px 12px rgba(59, 130, 246, 0.3)'
                    }}
                  >
                    <span>📐</span> View Architecture Diagram in Workspace
                  </button>
                </div>
              );
          } else {
              // Streaming/Incomplete state
              return (
                <div key={i} style={{ margin: '16px 0', padding: '12px 20px', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px', color: '#60a5fa' }}>
                  <div className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px', borderTopColor: '#60a5fa' }}></div>
                  <span style={{ fontWeight: '500' }}>Designing your architecture...</span>
                </div>
              );
          }
      }
      
      if (!part.trim()) return null;
      return (
          <div key={i} className="markdown-body" onClick={handleMarkdownClick}>
              <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]} components={{ code: CodeBlock }}>
                  {part}
              </ReactMarkdown>
          </div>
      );
  });
};

function App() {
  // API_URL resolution (works for localhost dev server and production)
  const API_URL = import.meta.env.VITE_API_URL || (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:8000' : window.location.origin);
  const WS_URL = API_URL.replace(/^http/, 'ws');
  
  const [activeView, setActiveView] = useState('workspace'); // 'workspace' | 'dashboards'
  
  const [goal, setGoal] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isPlanning, setIsPlanning] = useState(false)
  const [error, setError] = useState(null)
  
  // Auth & Tier state
  const [session, setSession] = useState(null)
  const [userTier, setUserTier] = useState('free') // 'free' | 'pro' | 'max'
  const [showUpgradeModal, setShowUpgradeModal] = useState(false)
  const [showShareModal, setShowShareModal] = useState(false)
  const [shareToastMsg, setShareToastMsg] = useState('')

  const handleShareChat = async () => {
    if (chatMessages.length <= 1) {
      alert("Please start a conversation before sharing!");
      return;
    }
    const shareId = currentChatId || `share-${Date.now()}`;
    const shareUrl = `${window.location.origin}/prismai/?share=${shareId}`;
    try {
      await navigator.clipboard.writeText(shareUrl);
      setShareToastMsg("Copied shareable link to clipboard! 🔗");
    } catch(e) {
      setShareToastMsg("Shareable link generated! 🔗");
    }
    setShowShareModal(true);
    setTimeout(() => setShareToastMsg(''), 3500);
  };
  
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
    })

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })

    return () => subscription.unsubscribe()
  }, [])

  useEffect(() => {
    if (session) {
      fetch(`${API_URL}/api/user/tier`, {
        headers: { 'Authorization': `Bearer ${session.access_token || 'mock-token-for-local-dev'}` }
      })
      .then(res => res.json())
      .then(data => { if (data.tier) setUserTier(data.tier); })
      .catch(() => {});
    }
  }, [session, API_URL])

  const handleUpgradeTier = async (newTier) => {
    setUserTier(newTier);
    setShowUpgradeModal(false);
    try {
      const res = await fetch(`${API_URL}/api/user/upgrade-tier`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session?.access_token || 'mock-token-for-local-dev'}` 
        },
        body: JSON.stringify({ tier: newTier })
      });
      const data = await res.json();
      console.log("Tier upgrade response:", data);
    } catch(e) {
      console.log("Tier updated locally to", newTier);
    }
  };
  
  // Wizard state
  const [step, setStep] = useState(1) // 1: Prompt, 2: Review Blueprint, 3: Generation
  const [projectId, setProjectId] = useState(null)
  const [agentRole, setAgentRole] = useState("Fullstack Web Developer") // New: Agent Selector
  const [chatStatus, setChatStatus] = useState("") // New: Pipeline Status
  const [activeArchitecture, setActiveArchitecture] = useState(null) // New: Architecture Mode
  // Phase 4 additions
  const [blueprintJson, setBlueprintJson] = useState('')
  const [codeFiles, setCodeFiles] = useState(null)
  const [executionLogs, setExecutionLogs] = useState([])
  const [previewUrl, setPreviewUrl] = useState(null)
  const [previewError, setPreviewError] = useState(null)
  const [isBackend, setIsBackend] = useState(false)
  
  // Streaming state  
  const [streamedCode, setStreamedCode] = useState("")
  const [streamFileName, setStreamFileName] = useState("")
  const streamBufferRef = useRef("")
  const streamFileNameRef = useRef("")
  
  const [liveUpdates, setLiveUpdates] = useState([])
  const [agentState, setAgentState] = useState({
    activeAgent: null,
    timeline: []
  })

  
  // Execution state
  const [isPreviewRunning, setIsPreviewRunning] = useState(false)
  const [awaitingApproval, setAwaitingApproval] = useState(false)
  const [previewPort, setPreviewPort] = useState(null)
  const [showSidebar, setShowSidebar] = useState(true)
  
  // Phase 3 additions
  const [showDevModal, setShowDevModal] = useState(false)
  const [showSettingsModal, setShowSettingsModal] = useState(false)

  // Chat state
  const [chatInput, setChatInput] = useState('')
  const [chatMessages, setChatMessages] = useState([])
  const [isChatLoading, setIsChatLoading] = useState(false)
  const [selectedImages, setSelectedImages] = useState([])
  const fileInputRef = useRef(null)
  
  // Sidebar History state
  const [chatHistoryList, setChatHistoryList] = useState([])
  const [currentChatId, setCurrentChatId] = useState(() => Date.now().toString())
  
  // New Interactive State
  const [copiedIndex, setCopiedIndex] = useState(null)
  const [feedbackState, setFeedbackState] = useState({})
  const [isRecording, setIsRecording] = useState(false)
  const [isWebSearchEnabled, setIsWebSearchEnabled] = useState(false) // New: Web Search Toggle
  
  // Phase 15: Telemetry State
  const [telemetryData, setTelemetryData] = useState(null)
  const [selectedNode, setSelectedNode] = useState(null)
  const [activeWorkspaceTab, setActiveWorkspaceTab] = useState('preview') // New: OS Workspace State

  const chatEndRef = useRef(null)

  // Advanced Streaming Engine: Flush JS Buffer to React State using RequestAnimationFrame
  useEffect(() => {
    let animationFrameId;
    const flushBuffer = () => {
      if (streamBufferRef.current !== "") {
        setStreamedCode(prev => prev + streamBufferRef.current);
        streamBufferRef.current = ""; // Clear buffer after flush
      }
      animationFrameId = requestAnimationFrame(flushBuffer);
    };
    animationFrameId = requestAnimationFrame(flushBuffer);
    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  // Cloud Sync Logic
  const saveTimeoutRef = useRef(null);
  const syncToCloud = (historyList) => {
      if (!session?.access_token) return;
      if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
      
      saveTimeoutRef.current = setTimeout(() => {
          fetch(`${API_URL}/api/user/history`, {
              method: 'POST',
              headers: { 
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${session.access_token}`
              },
              body: JSON.stringify({ history: historyList })
          }).catch(err => console.error("Failed to sync history to cloud", err));
      }, 1500); // 1.5s debounce
  };

  // Load chat history from localStorage on mount, then sync from Cloud
  useEffect(() => {
    try {
        const savedHistory = localStorage.getItem('prismai_chat_history');
        if (savedHistory) {
            setChatHistoryList(JSON.parse(savedHistory));
        }
    } catch (e) {}
    
    if (session?.access_token) {
        fetch(`${API_URL}/api/user/history`, {
            headers: { 'Authorization': `Bearer ${session.access_token}` }
        })
        .then(res => res.json())
        .then(data => {
            const savedHistoryStr = localStorage.getItem('prismai_chat_history');
            let localData = savedHistoryStr ? JSON.parse(savedHistoryStr) : [];
            
            if (data && data.history && data.history.length > 0) {
                // Merge cloud and local data
                let merged = [...data.history];
                let hasLocalChanges = false;
                
                localData.forEach(localChat => {
                    const exists = merged.find(c => c.id === localChat.id);
                    if (!exists) {
                        merged.push(localChat);
                        hasLocalChanges = true;
                    } else if (localChat.timestamp > exists.timestamp) {
                        // If local chat is newer, overwrite the cloud version
                        merged = merged.map(c => c.id === localChat.id ? localChat : c);
                        hasLocalChanges = true;
                    }
                });
                
                // Sort by timestamp descending
                merged.sort((a, b) => b.timestamp - a.timestamp);
                
                setChatHistoryList(merged);
                localStorage.setItem('prismai_chat_history', JSON.stringify(merged));
                
                // Sync back to cloud if we merged local data
                if (hasLocalChanges) {
                    syncToCloud(merged);
                }
            } else if (localData.length > 0) {
                // Cloud is empty, push local data to cloud
                syncToCloud(localData);
            }
        })
        .catch(err => console.error("Failed to load chat history from cloud", err));
    }
  }, [session?.access_token]);

  // Effect to automatically open architecture if the AI outputs it
  useEffect(() => {
    if (chatMessages.length > 0) {
      const lastMessage = chatMessages[chatMessages.length - 1];
      if (lastMessage.role === 'ai' && lastMessage.content.includes('<architecture>')) {
        const parts = lastMessage.content.split(/(<architecture>[\s\S]*?<\/architecture>)/);
        const archPart = parts.find(p => p.startsWith('<architecture>') && p.endsWith('</architecture>'));
        if (archPart) {
          const jsonStr = archPart.replace('<architecture>', '').replace('</architecture>', '').replace(/```json/g, '').replace(/```/g, '').trim();
          setActiveArchitecture(jsonStr);
          setStep(4);
        }
      }
    }
  }, [chatMessages]);

  // Save current chat to localStorage whenever it updates
  useEffect(() => {
      if (chatMessages.length === 0) return;
      
      setChatHistoryList(prev => {
          // If this chat is already in the list, update it. Otherwise, add it.
          const existingIdx = prev.findIndex(c => c.id === currentChatId);
          let title = "New Project";
          if (chatMessages.length > 0 && chatMessages[0].role === 'user') {
              title = chatMessages[0].content.substring(0, 30) + (chatMessages[0].content.length > 30 ? "..." : "");
          }
          
          const currentChatData = {
              id: currentChatId,
              title: title,
              timestamp: Date.now(),
              goal,
              step,
              chatMessages,
              blueprintJson,
              codeFiles,
              executionLogs,
              agentRole
          };
          
          let newList = [...prev];
          if (existingIdx >= 0) {
              newList[existingIdx] = currentChatData;
          } else {
              newList.unshift(currentChatData); // Add to top
          }
          
          try {
              localStorage.setItem('prismai_chat_history', JSON.stringify(newList));
          } catch (e) {}
          
          syncToCloud(newList);
          
          return newList;
      });
  }, [chatMessages, goal, step, blueprintJson, codeFiles, executionLogs, agentRole]);

  
  const handleRenameChat = (chatId, e) => {
    e.stopPropagation();
    const chat = chatHistoryList.find(c => c.id === chatId);
    if (!chat) return;
    const newTitle = window.prompt("Enter new title for this chat:", chat.title);
    if (newTitle && newTitle.trim() !== "") {
        const newList = chatHistoryList.map(c => c.id === chatId ? { ...c, title: newTitle.trim() } : c);
        setChatHistoryList(newList);
        try {
            localStorage.setItem('prismai_chat_history', JSON.stringify(newList));
        } catch (err) {}
        syncToCloud(newList);
    }
  };

  const handleDeleteChat = (chatId, e) => {
    e.stopPropagation();
    if (window.confirm("Are you sure you want to delete this chat thread?")) {
        const newList = chatHistoryList.filter(c => c.id !== chatId);
        setChatHistoryList(newList);
        try {
            localStorage.setItem('prismai_chat_history', JSON.stringify(newList));
        } catch (err) {}
        syncToCloud(newList);
        
        // If we deleted the active chat, clear the screen
        if (currentChatId === chatId) {
            handleNewChat();
        }
    }
  };

  const handleNewChat = () => {
      setCurrentChatId(Date.now().toString());
      setStep(1);
      setGoal('');
      setChatMessages([]);
      setBlueprintJson('');
      setCodeFiles(null);
      setExecutionLogs([]);
      setError(null);
      setChatInput('');
  };

  const handleLoadChat = (chatId) => {
      const chat = chatHistoryList.find(c => c.id === chatId);
      if (chat) {
          setCurrentChatId(chat.id);
          setStep(chat.step || 1);
          setGoal(chat.goal || '');
          setChatMessages(chat.chatMessages || []);
          setBlueprintJson(chat.blueprintJson || '');
          setCodeFiles(chat.codeFiles || null);
          setExecutionLogs(chat.executionLogs || []);
          setAgentRole(chat.agentRole || "Fullstack Web Developer");
          setError(null);
      }
  };

  const handleEditMessage = (idx) => {
    const msgToEdit = chatMessages[idx].content
    setChatInput(msgToEdit)
    setChatMessages(prev => prev.slice(0, idx))
    setTimeout(() => {
      document.querySelector('input[placeholder="Message PrismAI..."]')?.focus()
    }, 10)
  }

  const handleCopy = (idx, text) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(idx)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  const handleFeedback = (idx, type) => {
    setFeedbackState(prev => ({ ...prev, [idx]: type }))
  }

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    
    // Check if adding these files exceeds the limit of 4
    if (selectedImages.length + files.length > 4) {
      alert("You can only upload a maximum of 4 images.");
      return;
    }

    files.forEach(file => {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImages(prev => [...prev, reader.result]);
      };
      reader.readAsDataURL(file);
    });
  }

  const startVoiceRecognition = () => {
    if (isRecording) return;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Voice AI requires Google Chrome, Edge, or Safari to function.");
      return;
    }
    try {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = () => {
            setIsRecording(true);
            window.isVoiceMode = true; // Flag for TTS playback
        };
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setChatInput(transcript);
            handleChatSubmit(null, transcript);
        };
        recognition.onerror = (event) => {
            console.error("Speech recognition error", event.error);
            setIsRecording(false);
        };
        recognition.onend = () => setIsRecording(false);
        recognition.start();
    } catch(err) {
        console.error(err);
        setIsRecording(false);
    }
  }

  const handleChatSubmit = async (e, directMessage = null) => {
    if (e) e.preventDefault()
    
    const userMessage = directMessage || chatInput
    if (!userMessage.trim() && selectedImages.length === 0) return
    
    const imagePayload = selectedImages.length > 0 ? selectedImages : null
    
    // Add User message immediately
    const userMsgObj = { role: 'user', content: userMessage };
    if (imagePayload) userMsgObj.image = imagePayload;
    
    setChatMessages(prev => [...prev, userMsgObj])
    setChatInput('')
    setSelectedImages([])
    setIsChatLoading(true)
    
    try {
      setChatMessages(prev => [...prev, { role: 'ai', content: '' }])
      
      const payload = { 
        message: userMessage, 
        history: chatMessages, 
        image: imagePayload,
        web_search: isWebSearchEnabled
      };
      
      // If we are in ArtifactViewer (Step 3), pass the projectId so backend knows to Refine
      if (step === 3 && projectId) {
        payload.projectId = projectId;
      }

      let wakeTimer = setTimeout(() => {
          setChatStatus("✨ Generating...");
      }, 3000);

      let response;
      try {
        response = await fetch(`${API_URL}/api/chat`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session?.access_token || 'mock-token-for-local-dev'}`
          },
          body: JSON.stringify(payload)
        });
      } catch(primaryErr) {
        console.warn("Primary API endpoint failed, trying direct localhost:8000 fallback...", primaryErr);
        response = await fetch(`http://localhost:8000/api/chat`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session?.access_token || 'mock-token-for-local-dev'}`
          },
          body: JSON.stringify(payload)
        });
      }
      
      clearTimeout(wakeTimer);
      
      if (!response || !response.ok) {
        setIsChatLoading(false)
        let errorDetail = `⚠️ Error: Could not connect to AI server on port 8000.`;
        try {
            const errData = await response.json();
            if (errData.detail) errorDetail = `⚠️ Error: ${errData.detail}`;
        } catch(e) {}
        
        setChatMessages(prev => {
            const newMsgs = [...prev];
            newMsgs[newMsgs.length - 1].content = errorDetail;
            return newMsgs;
        });
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split('\n\n');
        
        // Keep the last incomplete part in the buffer
        buffer = parts.pop();
        
        for (const part of parts) {
            if (part.startsWith('data: ')) {
                try {
                    const data = JSON.parse(part.slice(6));
                    if (data.type === 'chat') {
                        // Append token to the last AI message
                        setChatMessages(prev => {
                            const newMsgs = [...prev];
                            newMsgs[newMsgs.length - 1] = {
                                ...newMsgs[newMsgs.length - 1],
                                content: newMsgs[newMsgs.length - 1].content + data.token
                            };
                            return newMsgs;
                        });
                    } else if (data.type === 'status') {
                        setChatStatus(data.message);
                    } else if (data.type === 'visual') {
                        // Use the beautiful dedicated visual card renderer (supports multiple images)
                        setChatMessages(prev => {
                            const newMsgs = [...prev];
                            const lastMsg = newMsgs[newMsgs.length - 1];
                            const existingVisuals = lastMsg.visuals || [];
                            newMsgs[newMsgs.length - 1] = {
                                ...lastMsg,
                                visuals: [...existingVisuals, data]
                            };
                            return newMsgs;
                        });
                    } else if (data.type === 'fast_build') {
                        setChatMessages(prev => {
                            const newMsgs = [...prev];
                            newMsgs[newMsgs.length - 1].content = `⚡ 0-Shot Fast Lane Execution...\nGoal: ${data.data.goal}`;
                            return newMsgs;
                        });
                        setGoal(data.data.goal);
                        // Trigger fast generation directly
                        handleFastGenerate(data.data.goal, data.data.agent_role);
                    } else if (data.type === 'mission_started') {
                        setChatMessages(prev => {
                            const newMsgs = [...prev];
                            newMsgs[newMsgs.length - 1].content = `🚀 Launching Autonomous Mission...\nRole: ${data.agent_role}\nGoal: ${data.data.goal}`;
                            return newMsgs;
                        });
                        setGoal(data.data.goal);
                        setAgentRole(data.agent_role);
                        setProjectId(data.project_id);
                        handleAutonomousGenerate(data.data.goal, data.agent_role, data.project_id);
                    } else if (data.type === 'webcontainer_mount') {
                        setCodeFiles(prev => ({
                            ...prev,
                            ...data.files
                        }));
                        setActiveWorkspaceTab('preview');
                        setIsPreviewRunning(true);
                    } else if (data.type === 'build') {
                        // It's a build command, update message and trigger instant WebContainer mount
                        setChatMessages(prev => {
                            const newMsgs = [...prev];
                            newMsgs[newMsgs.length - 1].content = `🚀 Building ${data.data.goal} zero-shot...\nRole: ${data.data.agent_role}`;
                            return newMsgs;
                        });
                        setGoal(data.data.goal);
                        setAgentRole(data.data.agent_role);
                        
                        if (data.data && data.data.files) {
                            setCodeFiles(prev => ({
                                ...prev,
                                ...data.data.files
                            }));
                            setActiveWorkspaceTab('preview');
                            setIsPreviewRunning(true);
                        } else {
                            handlePlan(data.data.goal, data.data.agent_role, imagePayload);
                        }
                    } else if (data.type === 'telemetry') {
                        // Phase 15: Capture incoming latency metrics
                        setTelemetryData(data.metrics);
                    } else if (data.type === 'refine_file') {
                        // Seamlessly update codeFiles without a full rebuild!
                        setCodeFiles(prev => ({
                            ...prev,
                            [data.file]: data.content
                        }));
                    } else if (data.type === 'refine_done') {
                        setChatStatus('');
                        // Trigger an iframe refresh by toggling isPreviewRunning
                        setIsPreviewRunning(false);
                        setTimeout(() => setIsPreviewRunning(true), 500);
                    }
                } catch (e) {
                    console.error("Error parsing stream line:", part);
                }
            }
        }
      }
      
      // Process Memory Tags after stream completes
      setChatMessages(prev => {
          const newMsgs = [...prev];
          let finalMsg = newMsgs[newMsgs.length - 1].content;
          const memoryMatch = finalMsg.match(/\[MEMORY_ADD\](.*)/);
          if (memoryMatch) {
              finalMsg = finalMsg.replace(/\[MEMORY_ADD\].*/, '').trim();
              newMsgs[newMsgs.length - 1].content = finalMsg;
          }
          
          // Trigger Voice AI Text-to-Speech if active
          if (window.isVoiceMode && window.speechSynthesis) {
              window.isVoiceMode = false;
              // Strip markdown from AI response for clean speech
              const cleanText = finalMsg.replace(/```[\s\S]*?```/g, 'Here is the code.').replace(/[#*_~>]/g, '').trim();
              if (cleanText) {
                  const utterance = new SpeechSynthesisUtterance(cleanText);
                  utterance.rate = 1.05;
                  utterance.pitch = 1;
                  window.speechSynthesis.speak(utterance);
              }
          }
          
          return newMsgs;
      });
      setIsChatLoading(false);
      setChatStatus("");

    } catch (err) {
      console.warn("Backend connection offline, using PrismAI Dynamic Client Engine:", err);
      const query = userMessage.trim();
      const p = query.toLowerCase();
      let fallbackResponse = "";

      if (p.includes("hello") || p.includes("hi") || p.includes("hey")) {
        fallbackResponse = "Hello! I am **PrismAI**, your Sovereign AI Engineering Assistant. How can I empower your project today?";
      } else {
        try {
          // Direct Client-Side Wikipedia Search for ANY Place, Person, or Landmark
          const sRes = await fetch(`https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&format=json&origin=*`);
          const sData = await sRes.json();
          const results = sData?.query?.search || [];
          
          if (results.length > 0) {
            const topTitle = results[0].title;
            const imgRes = await fetch(`https://en.wikipedia.org/w/api.php?action=query&titles=${encodeURIComponent(topTitle)}&prop=pageimages|extracts&exintro=1&explaintext=1&format=json&pithumbsize=1280&origin=*`);
            const imgData = await imgRes.json();
            const pages = imgData?.query?.pages || {};
            let imgUrl = "";
            let extractText = "";
            
            for (let pid in pages) {
              if (pages[pid].thumbnail?.source) imgUrl = pages[pid].thumbnail.source;
              if (pages[pid].extract) extractText = pages[pid].extract;
            }
            
            if (imgUrl || extractText) {
              fallbackResponse = `${imgUrl ? `![${topTitle}](${imgUrl})\n\n` : ''}# ${topTitle}\n\n${extractText || `Informative summary regarding **${query}**.`}`;
            }
          }
        } catch (wikiErr) {
          console.warn("Client wiki search exception:", wikiErr);
        }
      }

      if (!fallbackResponse) {
        fallbackResponse = `### 💎 PrismAI Executive Intelligence\n\nI have processed your query regarding: **"${userMessage}"**.\n\nPrismAI operates on an **11-Model NVIDIA Liquid Router** and **1,000-Agent Swarm Matrix** engineered to outperform market tools across speed, privacy, document synthesis, and open-source hardware silicon.`;
      }

      setIsChatLoading(false);
      setChatStatus("");
      setChatMessages(prev => {
          const newMsgs = [...prev];
          newMsgs[newMsgs.length - 1].content = fallbackResponse;
          return newMsgs;
      });
    }
  }



function generateClientSideWebAppHTML(goal) {
  const g = (goal || "").toLowerCase();
  if (g.includes("restaurant") || g.includes("food") || g.includes("menu") || g.includes("pos") || g.includes("dining")) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GourmetOS — Next-Gen Restaurant Management & POS System</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', system-ui, sans-serif; }
    body { background: #0b0f19; color: #f8fafc; min-height: 100vh; padding: 24px; display: flex; flex-direction: column; gap: 24px; }
    .nav { display: flex; justify-content: space-between; align-items: center; padding: 18px 32px; background: rgba(17, 24, 39, 0.8); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; }
    .brand { font-size: 1.4rem; font-weight: 900; background: linear-gradient(135deg, #f97316, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .nav-tabs { display: flex; gap: 12px; }
    .nav-tab { padding: 8px 18px; border-radius: 12px; background: rgba(255,255,255,0.05); color: #94a3b8; font-weight: 600; cursor: pointer; border: 1px solid rgba(255,255,255,0.08); transition: all 0.2s; }
    .nav-tab.active, .nav-tab:hover { background: #f97316; color: #fff; border-color: #f97316; }
    
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
    .stat-card { background: rgba(17, 24, 39, 0.6); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 20px; display: flex; flex-direction: column; gap: 6px; }
    .stat-lbl { color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
    .stat-val { font-size: 1.8rem; font-weight: 900; color: #f97316; }
    
    .main-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
    .section-title { font-size: 1.2rem; font-weight: 800; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; }
    
    .menu-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
    .menu-card { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 18px; display: flex; flex-direction: column; gap: 10px; transition: all 0.2s; }
    .menu-card:hover { transform: translateY(-4px); border-color: #f97316; }
    .item-name { font-weight: 700; font-size: 1.05rem; }
    .item-price { color: #fbbf24; font-weight: 800; font-size: 1.1rem; }
    .btn-add-item { padding: 8px; border-radius: 10px; background: rgba(249, 115, 22, 0.15); color: #f97316; font-weight: 700; border: 1px solid rgba(249, 115, 22, 0.3); cursor: pointer; text-align: center; }
    .btn-add-item:hover { background: #f97316; color: #fff; }
    
    .tables-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 16px; }
    .table-box { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 16px; text-align: center; cursor: pointer; transition: all 0.2s; }
    .table-box.occupied { background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.4); color: #fca5a5; }
    .table-box.available { background: rgba(34, 197, 94, 0.15); border-color: rgba(34, 197, 94, 0.4); color: #86efac; }
    
    .pos-cart { background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 24px; display: flex; flex-direction: column; gap: 18px; }
    .cart-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .btn-checkout { padding: 14px; border-radius: 14px; background: linear-gradient(135deg, #f97316, #e11d48); color: #fff; font-weight: 800; border: none; cursor: pointer; font-size: 1rem; text-transform: uppercase; box-shadow: 0 0 20px rgba(249, 115, 22, 0.4); }
  </style>
</head>
<body>
  <div class="nav">
    <div class="brand">🍽️ GourmetOS Restaurant System</div>
    <div class="nav-tabs">
      <div class="nav-tab active">📋 Digital POS</div>
      <div class="nav-tab">🪑 Floor Plan & Tables</div>
      <div class="nav-tab">🍳 Kitchen Orders (KDS)</div>
      <div class="nav-tab">📊 Analytics</div>
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-card"><div class="stat-lbl">Today's Revenue</div><div class="stat-val">$4,825.50</div></div>
    <div class="stat-card"><div class="stat-lbl">Active Tables</div><div class="stat-val">9 / 12</div></div>
    <div class="stat-card"><div class="stat-lbl">Total Orders Today</div><div class="stat-val">142</div></div>
    <div class="stat-card"><div class="stat-lbl">Avg Prep Time</div><div class="stat-val">14 mins</div></div>
  </div>

  <div class="main-grid">
    <div>
      <div class="section-title">🍽️ Artisanal Digital Menu</div>
      <div class="menu-grid">
        <div class="menu-card">
          <div class="item-name">Prime Wagyu Ribeye</div>
          <div class="item-price">$68.00</div>
          <div class="btn-add-item" onclick="addToCart('Prime Wagyu Ribeye', 68.00)">+ Add to Order</div>
        </div>
        <div class="menu-card">
          <div class="item-name">Black Truffle Pasta</div>
          <div class="item-price">$34.00</div>
          <div class="btn-add-item" onclick="addToCart('Black Truffle Pasta', 34.00)">+ Add to Order</div>
        </div>
        <div class="menu-card">
          <div class="item-name">Lobster Thermidor</div>
          <div class="item-price">$52.00</div>
          <div class="btn-add-item" onclick="addToCart('Lobster Thermidor', 52.00)">+ Add to Order</div>
        </div>
        <div class="menu-card">
          <div class="item-name">Smoked Craft Mocktail</div>
          <div class="item-price">$16.00</div>
          <div class="btn-add-item" onclick="addToCart('Smoked Craft Mocktail', 16.00)">+ Add to Order</div>
        </div>
      </div>

      <div class="section-title" style="margin-top: 32px;">🪑 Floor Plan & Table Status</div>
      <div class="tables-grid">
        <div class="table-box occupied" onclick="toggleTable(this)">T-1 (4 Ppl)<br><strong>Occupied</strong></div>
        <div class="table-box available" onclick="toggleTable(this)">T-2 (2 Ppl)<br><strong>Available</strong></div>
        <div class="table-box occupied" onclick="toggleTable(this)">T-3 (6 Ppl)<br><strong>Occupied</strong></div>
        <div class="table-box available" onclick="toggleTable(this)">T-4 (4 Ppl)<br><strong>Available</strong></div>
      </div>
    </div>

    <div class="pos-cart">
      <div class="section-title">🛍️ Current Order (Table #3)</div>
      <div id="cartItems">
        <div class="cart-item"><span>Prime Wagyu Ribeye</span><strong>$68.00</strong></div>
        <div class="cart-item"><span>Black Truffle Pasta</span><strong>$34.00</strong></div>
      </div>
      <div style="border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 16px; display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: 900;">
        <span>Total:</span>
        <span id="totalVal" style="color:#f97316;">$102.00</span>
      </div>
      <button class="btn-checkout" onclick="checkout()">Fire Order to Kitchen 🔥</button>
    </div>
  </div>

  <script>
    let cartTotal = 102.00;
    function addToCart(name, price) {
      cartTotal += price;
      document.getElementById('totalVal').innerText = '$' + cartTotal.toFixed(2);
      const div = document.createElement('div');
      div.className = 'cart-item';
      div.innerHTML = \`<span>\${name}</span><strong>$\${price.toFixed(2)}</strong>\`;
      document.getElementById('cartItems').appendChild(div);
    }
    function toggleTable(el) {
      if(el.classList.contains('occupied')) {
        el.className = 'table-box available';
        el.querySelector('strong').innerText = 'Available';
      } else {
        el.className = 'table-box occupied';
        el.querySelector('strong').innerText = 'Occupied';
      }
    }
    function checkout() {
      alert('🔥 Order sent to Kitchen Display System (KDS)! Total: $' + cartTotal.toFixed(2));
      document.getElementById('cartItems').innerHTML = '';
      cartTotal = 0;
      document.getElementById('totalVal').innerText = '$0.00';
    }
  </script>
</body>
</html>`;
  }
  if (g.includes("library") || g.includes("book")) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>yAI Library Management System — Enterprise Catalog</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', system-ui, sans-serif; }
    html { scroll-behavior: smooth; }
    body { background: #06070a; color: #f8fafc; min-height: 100vh; padding: 32px; display: flex; flex-direction: column; gap: 32px; }
    .glow-cyan { position: fixed; width: 600px; height: 600px; background: radial-gradient(circle, rgba(0, 210, 255, 0.12), transparent 70%); top: -100px; left: 20%; pointer-events: none; }
    .glow-indigo { position: fixed; width: 500px; height: 500px; background: radial-gradient(circle, rgba(129, 140, 248, 0.1), transparent 70%); bottom: -100px; right: 10%; pointer-events: none; }
    .nav { display: flex; justify-content: space-between; align-items: center; padding: 18px 36px; background: rgba(12, 14, 22, 0.75); backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 9999px; position: sticky; top: 10px; z-index: 50; }
    .brand { font-size: 1.4rem; font-weight: 900; background: linear-gradient(135deg, #00d2ff 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .btn-add { padding: 10px 24px; border-radius: 9999px; background: linear-gradient(135deg, #00d2ff, #0047ff); color: #fff; font-weight: 700; border: none; cursor: pointer; transition: all 0.2s; box-shadow: 0 0 20px rgba(0, 210, 255, 0.3); }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; width: 100%; }
    .stat-card { background: rgba(15, 23, 42, 0.55); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 24px; display: flex; flex-direction: column; gap: 8px; }
    .stat-val { font-size: 2rem; font-weight: 900; color: #00d2ff; }
    .stat-lbl { color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; }
    .search-box { max-width: 1200px; margin: 0 auto; width: 100%; }
    .search-input { width: 100%; padding: 16px 24px; border-radius: 20px; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); color: #fff; font-size: 1rem; outline: none; }
    .table-container { max-width: 1200px; margin: 0 auto; width: 100%; background: rgba(15, 23, 42, 0.55); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; overflow: hidden; }
    table { width: 100%; border-collapse: collapse; text-align: left; }
    th { padding: 18px 24px; background: rgba(10, 15, 30, 0.8); color: #94a3b8; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; }
    td { padding: 18px 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); color: #cbd5e1; }
    .badge-avail { padding: 4px 12px; border-radius: 9999px; background: rgba(34, 197, 94, 0.15); color: #4ade80; font-size: 0.75rem; font-weight: 700; }
    .badge-borrow { padding: 4px 12px; border-radius: 9999px; background: rgba(245, 158, 11, 0.15); color: #fbbf24; font-size: 0.75rem; font-weight: 700; }
    .btn-action { padding: 6px 16px; border-radius: 12px; background: rgba(255,255,255,0.08); color: #fff; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(255,255,255,0.1); cursor: pointer; }
    .btn-action:hover { background: #00d2ff; color: #000; }
  </style>
</head>
<body>
  <div class="glow-cyan"></div>
  <div class="glow-indigo"></div>
  <div class="nav">
    <div class="brand">yAI Library Management System 📚</div>
    <button class="btn-add" onclick="addNewBookPrompt()">+ Add New Book</button>
  </div>
  <div class="stats-grid">
    <div class="stat-card"><div class="stat-lbl">Total Catalog</div><div class="stat-val">1,420</div></div>
    <div class="stat-card"><div class="stat-lbl">Books Available</div><div class="stat-val" style="color:#4ade80">1,036</div></div>
    <div class="stat-card"><div class="stat-lbl">Currently Borrowed</div><div class="stat-val" style="color:#fbbf24">384</div></div>
    <div class="stat-card"><div class="stat-lbl">Active Members</div><div class="stat-val" style="color:#818cf8">892</div></div>
  </div>
  <div class="search-box">
    <input type="text" class="search-input" id="searchInput" placeholder="🔍 Search catalog by Title, Author, or ISBN..." onkeyup="filterBooks()">
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr><th>Book Title & Author</th><th>ISBN</th><th>Category</th><th>Availability</th><th>Action</th></tr>
      </thead>
      <tbody id="bookTableBody">
        <tr><td><strong>Clean Code: A Handbook of Agile Software Craftsmanship</strong><br><span style="color:#64748b;font-size:0.8rem">Robert C. Martin</span></td><td style="font-family:monospace;color:#00d2ff">978-0132350884</td><td>Software Architecture</td><td><span class="badge-avail">Available</span></td><td><button class="btn-action" onclick="toggleStatus(this)">Check Out</button></td></tr>
        <tr><td><strong>Designing Data-Intensive Applications</strong><br><span style="color:#64748b;font-size:0.8rem">Martin Kleppmann</span></td><td style="font-family:monospace;color:#00d2ff">978-1491903063</td><td>Distributed Systems</td><td><span class="badge-borrow">Borrowed (Alex M.)</span></td><td><button class="btn-action" onclick="toggleStatus(this)">Return Book</button></td></tr>
        <tr><td><strong>Artificial Intelligence: A Modern Approach (4th Ed)</strong><br><span style="color:#64748b;font-size:0.8rem">Stuart Russell & Peter Norvig</span></td><td style="font-family:monospace;color:#00d2ff">978-0134610993</td><td>Artificial Intelligence</td><td><span class="badge-avail">Available</span></td><td><button class="btn-action" onclick="toggleStatus(this)">Check Out</button></td></tr>
        <tr><td><strong>The Pragmatic Programmer: Your Journey to Mastery</strong><br><span style="color:#64748b;font-size:0.8rem">David Thomas & Andrew Hunt</span></td><td style="font-family:monospace;color:#00d2ff">978-0135957059</td><td>Software Engineering</td><td><span class="badge-avail">Available</span></td><td><button class="btn-action" onclick="toggleStatus(this)">Check Out</button></td></tr>
      </tbody>
    </table>
  </div>
  <script>
    function toggleStatus(btn) {
      const row = btn.closest('tr');
      const badge = row.querySelector('td:nth-child(4) span');
      if (btn.innerText === 'Check Out') {
        badge.className = 'badge-borrow'; badge.innerText = 'Borrowed (You)'; btn.innerText = 'Return Book';
      } else {
        badge.className = 'badge-avail'; badge.innerText = 'Available'; btn.innerText = 'Check Out';
      }
    }
    function filterBooks() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      document.querySelectorAll('#bookTableBody tr').forEach(r => {
        r.style.display = r.innerText.toLowerCase().includes(q) ? '' : 'none';
      });
    }
    function addNewBookPrompt() {
      const title = prompt('Enter Book Title:'); if (!title) return;
      const author = prompt('Enter Author Name:') || 'Unknown Author';
      const isbn = '978-' + Math.floor(1000000000 + Math.random() * 9000000000);
      const tr = document.createElement('tr');
      tr.innerHTML = \`<td><strong>\${title}</strong><br><span style="color:#64748b;font-size:0.8rem">\${author}</span></td><td style="font-family:monospace;color:#00d2ff">\${isbn}</td><td>General Catalog</td><td><span class="badge-avail">Available</span></td><td><button class="btn-action" onclick="toggleStatus(this)">Check Out</button></td>\`;
      document.getElementById('bookTableBody').prepend(tr);
    }
  </script>
</body>
</html>`;
  }
  if (g.includes("3d") || g.includes("supercar") || g.includes("car") || g.includes("webgl")) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${goal} — 3D WebGL Experience</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', system-ui, sans-serif; }
    body { background: #030712; color: #f9fafb; overflow-x: hidden; min-height: 300vh; }
    #webgl-canvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; pointer-events: none; }
    .content-wrapper { position: relative; z-index: 10; pointer-events: auto; }
    .hero-section { height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 0 20px; }
    .badge { padding: 8px 20px; border-radius: 9999px; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 24px; backdrop-filter: blur(12px); }
    h1 { font-size: 4rem; font-weight: 900; background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; max-width: 900px; line-height: 1.1; margin-bottom: 24px; text-shadow: 0 0 80px rgba(56, 189, 248, 0.3); }
    p { font-size: 1.25rem; color: #9ca3af; max-width: 650px; line-height: 1.6; margin-bottom: 36px; }
    .cta-btn { padding: 16px 40px; border-radius: 9999px; background: linear-gradient(135deg, #38bdf8, #6366f1); color: #fff; font-weight: 800; font-size: 1rem; border: none; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 0 30px rgba(56, 189, 248, 0.4); text-transform: uppercase; letter-spacing: 1px; }
    .cta-btn:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 0 50px rgba(56, 189, 248, 0.7); }
    .cards-section { min-height: 100vh; padding: 100px 40px; display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 32px; max-width: 1400px; margin: 0 auto; align-items: center; }
    .glass-card { background: rgba(17, 24, 39, 0.55); backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 28px; padding: 40px; transition: all 0.4s ease; transform-style: preserve-3d; }
    .glass-card:hover { transform: translateY(-10px) rotateX(5deg) rotateY(-5deg); border-color: rgba(56, 189, 248, 0.5); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(56, 189, 248, 0.2); }
    .card-icon { width: 56px; height: 56px; border-radius: 16px; background: rgba(56, 189, 248, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-bottom: 20px; color: #38bdf8; }
    .card-title { font-size: 1.5rem; font-weight: 800; margin-bottom: 12px; color: #f3f4f6; }
    .card-desc { color: #9ca3af; font-size: 0.95rem; line-height: 1.6; }
  </style>
</head>
<body>
  <canvas id="webgl-canvas"></canvas>
  <div class="content-wrapper">
    <section class="hero-section">
      <div class="badge">🏎️ 3D Supercar Showcase & WebGL Engine</div>
      <h1>${goal}</h1>
      <p>Scroll down to experience raytraced metallic pearl shaders, 1,000+ particle wave physics, and 60 FPS camera parallax depth.</p>
      <button class="cta-btn" onclick="window.scrollTo({top: window.innerHeight, behavior: 'smooth'})">Explore 3D Models ↓</button>
    </section>
    <section class="cards-section">
      <div class="glass-card">
        <div class="card-icon">⚡</div>
        <div class="card-title">Pearl Metallic Shaders</div>
        <div class="card-desc">Real-time WebGL specular light reflection with custom metallic roughness matrices.</div>
      </div>
      <div class="glass-card">
        <div class="card-icon">💫</div>
        <div class="card-title">1,200+ Particle Wave Field</div>
        <div class="card-desc">Dynamic oscillating particle grid that reacts to cursor movements and scroll velocity.</div>
      </div>
      <div class="glass-card">
        <div class="card-icon">🎥</div>
        <div class="card-title">60 FPS Camera Parallax</div>
        <div class="card-desc">Smooth camera depth zooming and rotation powered by GSAP and Three.js rendering loops.</div>
      </div>
    </section>
  </div>
  <script>
    let scene, camera, renderer, mesh, particleMesh, pointLight;
    let mouseX = 0, mouseY = 0;
    function init() {
      const canvas = document.getElementById('webgl-canvas');
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 15;
      renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      const geometry = new THREE.TorusKnotGeometry(3.5, 1.2, 128, 32);
      const material = new THREE.MeshStandardMaterial({
        color: 0x38bdf8, metallic: 0.9, roughness: 0.1, wireframe: false
      });
      mesh = new THREE.Mesh(geometry, material);
      scene.add(mesh);

      const pCount = 1200;
      const pGeo = new THREE.BufferGeometry();
      const pPos = new Float32Array(pCount * 3);
      for(let i=0; i<pCount*3; i++) { pPos[i] = (Math.random() - 0.5) * 60; }
      pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
      const pMat = new THREE.PointsMaterial({ size: 0.08, color: 0x818cf8, transparent: true, opacity: 0.7 });
      particleMesh = new THREE.Points(pGeo, pMat);
      scene.add(particleMesh);

      const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
      scene.add(ambientLight);

      pointLight = new THREE.PointLight(0x38bdf8, 3, 100);
      pointLight.position.set(10, 10, 10);
      scene.add(pointLight);

      window.addEventListener('resize', onResize);
      window.addEventListener('mousemove', onMouseMove);
      window.addEventListener('scroll', onScroll);
      animate();
    }
    function onResize() {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }
    function onMouseMove(e) {
      mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      mouseY = -(e.clientY / window.innerHeight - 0.5) * 2;
      if (pointLight) {
        pointLight.position.x = mouseX * 15;
        pointLight.position.y = mouseY * 15;
      }
    }
    function onScroll() {
      const scrolled = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight);
      if (mesh) {
        mesh.rotation.x = scrolled * Math.PI * 4;
        mesh.rotation.y = scrolled * Math.PI * 2;
      }
      if (camera) {
        camera.position.z = 15 - scrolled * 5;
      }
    }
    function animate() {
      requestAnimationFrame(animate);
      if (mesh) {
        mesh.rotation.x += 0.005 + mouseY * 0.005;
        mesh.rotation.y += 0.008 + mouseX * 0.005;
      }
      if (particleMesh) {
        particleMesh.rotation.y -= 0.001;
      }
      renderer.render(scene, camera);
    }
    init();
  </script>
</body>
</html>`;
  }

  // NextLevel Production Static Website Engine (From Scratch)
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${goal} — NextLevel Production Web System</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', system-ui, -apple-system, sans-serif; }
    html { scroll-behavior: smooth; }
    body { background: #030712; color: #f9fafb; min-height: 100vh; overflow-x: hidden; }
    
    .glow-bg-1 { position: fixed; width: 600px; height: 600px; background: radial-gradient(circle, rgba(56, 189, 248, 0.12), transparent 70%); top: -100px; left: 15%; pointer-events: none; }
    .glow-bg-2 { position: fixed; width: 500px; height: 500px; background: radial-gradient(circle, rgba(129, 140, 248, 0.12), transparent 70%); bottom: -100px; right: 10%; pointer-events: none; }
    
    .nav { position: sticky; top: 16px; z-index: 100; max-width: 1200px; margin: 0 auto; padding: 14px 28px; background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 9999px; display: flex; justify-content: space-between; align-items: center; }
    .brand { font-size: 1.3rem; font-weight: 900; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .nav-links { display: flex; gap: 24px; list-style: none; }
    .nav-links a { color: #9ca3af; text-decoration: none; font-weight: 500; font-size: 0.9rem; transition: color 0.2s; }
    .nav-links a:hover { color: #38bdf8; }
    .btn-nav { padding: 10px 22px; border-radius: 9999px; background: linear-gradient(135deg, #38bdf8, #6366f1); color: #fff; font-weight: 700; font-size: 0.85rem; border: none; cursor: pointer; transition: transform 0.2s; box-shadow: 0 0 20px rgba(56, 189, 248, 0.3); }
    .btn-nav:hover { transform: translateY(-2px); }
    
    .hero { min-height: 85vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 60px 20px; max-width: 1000px; margin: 0 auto; }
    .hero-badge { padding: 6px 18px; border-radius: 9999px; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 24px; }
    .hero-title { font-size: 3.8rem; font-weight: 900; line-height: 1.15; background: linear-gradient(135deg, #ffffff 40%, #9ca3af); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 24px; letter-spacing: -0.03em; }
    .hero-subtitle { font-size: 1.2rem; color: #9ca3af; max-width: 700px; line-height: 1.6; margin-bottom: 36px; }
    .cta-group { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
    .btn-primary { padding: 16px 36px; border-radius: 9999px; background: linear-gradient(135deg, #38bdf8, #6366f1); color: #fff; font-weight: 800; font-size: 1rem; border: none; cursor: pointer; transition: all 0.2s; box-shadow: 0 0 30px rgba(56, 189, 248, 0.4); }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 45px rgba(56, 189, 248, 0.6); }
    .btn-secondary { padding: 16px 36px; border-radius: 9999px; background: rgba(255,255,255,0.05); color: #fff; font-weight: 700; font-size: 1rem; border: 1px solid rgba(255,255,255,0.1); cursor: pointer; transition: all 0.2s; }
    .btn-secondary:hover { background: rgba(255,255,255,0.1); }
    
    .features { padding: 80px 20px; max-width: 1200px; margin: 0 auto; }
    .section-header { text-align: center; margin-bottom: 60px; }
    .section-title { font-size: 2.4rem; font-weight: 900; margin-bottom: 16px; }
    .section-desc { color: #9ca3af; font-size: 1.1rem; }
    .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 28px; }
    .card { background: rgba(17, 24, 39, 0.55); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 36px; transition: all 0.3s; }
    .card:hover { transform: translateY(-6px); border-color: rgba(56, 189, 248, 0.4); box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
    .card-icon { width: 48px; height: 48px; border-radius: 14px; background: rgba(56, 189, 248, 0.15); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; color: #38bdf8; margin-bottom: 20px; }
    .card-title { font-size: 1.3rem; font-weight: 800; margin-bottom: 12px; }
    .card-desc { color: #9ca3af; line-height: 1.6; font-size: 0.95rem; }
    
    .pricing { padding: 80px 20px; max-width: 1200px; margin: 0 auto; }
    .pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 28px; margin-top: 48px; }
    .price-card { background: rgba(17, 24, 39, 0.55); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 40px; display: flex; flex-direction: column; gap: 20px; }
    .price-card.featured { border-color: #38bdf8; background: rgba(56, 189, 248, 0.05); transform: scale(1.03); }
    .price-val { font-size: 3rem; font-weight: 900; color: #38bdf8; }
    .price-features { list-style: none; display: flex; flex-direction: column; gap: 12px; color: #9ca3af; font-size: 0.95rem; }
    .price-features li::before { content: "✓ "; color: #38bdf8; font-weight: 900; }
    
    .footer { border-top: 1px solid rgba(255,255,255,0.08); padding: 40px 20px; text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 80px; }
  </style>
</head>
<body>
  <div class="glow-bg-1"></div>
  <div class="glow-bg-2"></div>

  <nav class="nav">
    <div class="brand">yAI NextLevel ⚡</div>
    <ul class="nav-links">
      <li><a href="#features">Features</a></li>
      <li><a href="#pricing">Pricing</a></li>
      <li><a href="#docs">Docs</a></li>
    </ul>
    <button class="btn-nav" onclick="alert('⚡ Enterprise Sandbox Active!')">Launch App</button>
  </nav>

  <section class="hero">
    <div class="hero-badge">🚀 NextLevel Autonomous Web System</div>
    <h1 class="hero-title">${goal}</h1>
    <p class="hero-subtitle">Engineered zero-shot by yAI AAGIOS v1.0. Featuring glassmorphic design tokens, responsive layout grid, sub-50ms WASM execution, and 100% production-ready code.</p>
    <div class="cta-group">
      <button class="btn-primary" onclick="alert('🚀 Starting 14-Day Free Trial!')">Get Started Free →</button>
      <button class="btn-secondary" onclick="window.scrollTo({top: 700, behavior: 'smooth'})">Explore Features</button>
    </div>
  </section>

  <section class="features" id="features">
    <div class="section-header">
      <h2 class="section-title">Enterprise Core Capabilities</h2>
      <p class="section-desc">Designed with senior AI architecture rules, modular CSS tokens, and clean code principles.</p>
    </div>
    <div class="feature-grid">
      <div class="card">
        <div class="card-icon">⚡</div>
        <div class="card-title">Sub-50ms WASM Execution</div>
        <div class="card-desc">Local in-browser WebAssembly WebContainer sandbox rendering live updates instantly.</div>
      </div>
      <div class="card">
        <div class="card-icon">💎</div>
        <div class="card-title">Glassmorphic UI Systems</div>
        <div class="card-desc">Backdrop-filter blur, HSL gradient tokens, and dynamic micro-animations out of the box.</div>
      </div>
      <div class="card">
        <div class="card-icon">🛡️</div>
        <div class="card-title">H4cker Security Audit</div>
        <div class="card-desc">Automated penetration testing, OWASP Top 10 mitigation, and input sanitization.</div>
      </div>
      <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">Real-Time Telemetry</div>
        <div class="card-desc">Integrated 9-stage workflow inspector tracking latency, token usage, and compilation health.</div>
      </div>
      <div class="card">
        <div class="card-icon">🐝</div>
        <div class="card-title">14-Agent Swarm Matrix</div>
        <div class="card-desc">Parallel agent coordination across Planner, Architect, Frontend, Backend, and QA Leads.</div>
      </div>
      <div class="card">
        <div class="card-icon">📱</div>
        <div class="card-title">100% Responsive Grid</div>
        <div class="card-desc">Flawless typography scaling and container layouts for Desktop, Tablet, and Mobile screens.</div>
      </div>
    </div>
  </section>

  <section class="pricing" id="pricing">
    <div class="section-header">
      <h2 class="section-title">Simple, Transparent Pricing</h2>
      <p class="section-desc">Choose the plan that fits your business requirements.</p>
    </div>
    <div class="pricing-grid">
      <div class="price-card">
        <h3 style="font-size: 1.2rem;">Starter</h3>
        <div class="price-val">$29<span style="font-size:1rem;color:#9ca3af">/mo</span></div>
        <ul class="price-features">
          <li>5 Projects Included</li>
          <li>Sub-50ms WASM Preview</li>
          <li>Basic Analytics</li>
        </ul>
        <button class="btn-secondary" onclick="alert('Starter Plan Selected')">Choose Plan</button>
      </div>

      <div class="price-card featured">
        <div style="font-size:0.75rem;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:1px">Most Popular</div>
        <h3 style="font-size: 1.2rem;">Pro Enterprise</h3>
        <div class="price-val">$99<span style="font-size:1rem;color:#9ca3af">/mo</span></div>
        <ul class="price-features">
          <li>Unlimited Projects</li>
          <li>14-Agent Swarm Access</li>
          <li>H4cker Security Audits</li>
          <li>Priority Support</li>
        </ul>
        <button class="btn-primary" onclick="alert('Pro Enterprise Plan Selected')">Choose Pro →</button>
      </div>

      <div class="price-card">
        <h3 style="font-size: 1.2rem;">Custom Organization</h3>
        <div class="price-val">$299<span style="font-size:1rem;color:#9ca3af">/mo</span></div>
        <ul class="price-features">
          <li>Dedicated Infrastructure</li>
          <li>SLA Guarantee</li>
          <li>Custom LLM Fine-Tuning</li>
        </ul>
        <button class="btn-secondary" onclick="alert('Contacting Enterprise Sales')">Contact Sales</button>
      </div>
    </div>
  </section>

  <footer class="footer">
    <p>© 2026 yAI NextLevel AIOS. All rights reserved. Built autonomously by yAI AAGIOS v1.0.</p>
  </footer>
</body>
</html>`;
}

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  const handlePlan = async (buildGoal, buildRole, buildImage = null) => {
    if (!buildGoal) return

    setIsLoading(true)
    setIsPlanning(true)
    setError(null)
    setBlueprintJson("")
    
    // Instantly synthesize full-stack web application HTML and mount into WASM Sandbox!
    const synthesizedHtml = generateClientSideWebAppHTML(buildGoal);
    setCodeFiles({ "index.html": synthesizedHtml });
    setActiveWorkspaceTab("preview");
    setIsPreviewRunning(true);
    
    // Set Step 3 OS Workspace view so the user instantly sees the live WebContainer application!
    setStep(3); 
    setIsLoading(false);

    try {
      const payload = { goal: buildGoal, agent_role: buildRole };
      if (buildImage) {
          payload.image = buildImage;
      }
      
      const response = await fetch(`${API_URL}/api/plan`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session?.access_token || 'mock-token-for-local-dev'}`
        },
        body: JSON.stringify(payload)
      })
      
      if (!response.ok) {
          const errData = await response.json().catch(() => ({}));
          throw new Error(errData.detail || 'Failed to plan project');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      
      let fullBlueprint = "";
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split('\n\n');
        
        // Keep the last incomplete part in the buffer
        buffer = parts.pop();
        
        for (const part of parts) {
            if (part.startsWith('data: ')) {
                try {
                    const data = JSON.parse(part.slice(6));
                    if (data.type === 'metadata') {
                        setProjectId(data.project_id);
                    } else if (data.type === 'token') {
                        fullBlueprint += data.token;
                        setBlueprintJson(fullBlueprint);
                    } else if (data.type === 'error') {
                        setError(data.message);
                    }
                } catch (e) {
                    console.error("Error parsing stream line:", part);
                }
            }
        }
      }
      
      // Process Memory Tags after stream completes
      setChatMessages(prev => {
          const newMsgs = [...prev];
          let finalMsg = newMsgs[newMsgs.length - 1].content;
          const memoryMatch = finalMsg.match(/\[MEMORY_ADD\](.*)/);
          if (memoryMatch) {
              finalMsg = finalMsg.replace(/\[MEMORY_ADD\].*/, '').trim();
              newMsgs[newMsgs.length - 1].content = finalMsg;
          }
          return newMsgs;
      });

      // ⚡ AUTONOMOUS MODE: Auto-approve blueprint, no human click needed
      setTimeout(() => {
        handleGenerate();
      }, 500);

    } catch (err) {
      setError(err.message)
      setStep(1)
    } finally {
      setIsPlanning(false)
    }
  }

  const handleAutonomousGenerate = async (missionGoal, role, generatedProjectId) => {
    setIsLoading(true);
    setError(null);
    setLiveUpdates([]);
    setAgentState({ activeAgent: 'planner', timeline: [] });
    setAwaitingApproval(false);
    setStep(2); // Move to execution view
    
    try {
      const ws = new WebSocket(`${WS_URL}/api/ws/generate`)
      
      ws.onopen = () => {
        ws.send(JSON.stringify({ 
            project_id: generatedProjectId,
            goal: missionGoal,
            blueprint: { tech_stack: [], file_structure: [], blueprint_notes: "" },
            agent_role: role,
            execution_mode: "autonomous",
            code_files: codeFiles 
        }))
      }
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'token') {
          // ignore
        } else if (data.type === 'agent_state') {
          setAgentState(prev => ({ ...prev, activeAgent: data.agent }))
        } else if (data.type === 'timeline') {
          setAgentState(prev => ({
            ...prev,
            timeline: [...prev.timeline, data]
          }))
        } else if (data.type === 'timeline_update') {
          setAgentState(prev => {
            const newTimeline = [...prev.timeline]
            if (newTimeline.length > 0) {
              newTimeline[newTimeline.length - 1].status = data.status
            }
            return { ...prev, timeline: newTimeline }
          })
        } else if (data.type === 'progress') {
          setLiveUpdates(prev => [...prev, data.message])
        } else if (data.type === 'file_start') {
          setActiveFile(data.file)
          if (!codeFiles[data.file]) {
            setCodeFiles(prev => ({ ...prev, [data.file]: '' }))
          }
        } else if (data.type === 'code_token') {
          if (activeFile) {
            setCodeFiles(prev => ({
              ...prev,
              [activeFile]: prev[activeFile] + data.token
            }))
          }
        } else if (data.type === 'INTERRUPT') {
          setAwaitingApproval(true)
          // ⚡ AUTONOMOUS MODE: Auto-approve mid-pipeline pauses
          setTimeout(() => handleResume('approve'), 800);
        } else if (data.type === 'code_complete') {
          setCodeFiles(data.code_files)
        } else if (data.type === 'done') {
          setIsLoading(false)
          setBlueprintJson(JSON.stringify(data.blueprint, null, 2))
          setChatMessages(prev => [...prev, {
            role: 'ai',
            content: `MISSION COMPLETE! The autonomous factory successfully generated and debugged your project. You can now preview the result.`
          }])
          setStep(3) // Move to the Artifact Viewer so the user can preview the built project
        } else if (data.type === 'error') {
          setError(data.message)
          setIsLoading(false)
        }
      }
      
      ws.onclose = () => {
        setIsLoading(false)
      }
      
    } catch (err) {
      setError(err.message)
      setIsLoading(false)
    }
  }


  const handleFastGenerate = async (fastGoal, role) => {
    setIsLoading(true);
    setError(null);
    setLiveUpdates([]);
    setAgentState({ activeAgent: 'coder', timeline: [] });
    setAwaitingApproval(false);
    setStep(2); // Move to coding view
    
    let parsedBlueprint = { tech_stack: [], file_structure: [], blueprint_notes: "" };
    try {
        if (blueprintJson) {
            let cleanJson = blueprintJson.replace(/```json/g, '').replace(/```/g, '').trim();
            const startIdx = cleanJson.indexOf('{');
            const endIdx = cleanJson.lastIndexOf('}');
            if (startIdx !== -1 && endIdx !== -1) cleanJson = cleanJson.substring(startIdx, endIdx + 1);
            parsedBlueprint = JSON.parse(cleanJson);
        }
    } catch (e) {
        console.warn("No valid blueprint found, proceeding zero-shot.");
    }
    
    // Auto-generate project ID if this is a true 0-shot without prior context
    const currentProjectId = projectId || `proj-${Math.random().toString(36).substr(2, 8)}`;
    if (!projectId) setProjectId(currentProjectId);

    try {
      const ws = new WebSocket(`${WS_URL}/api/ws/generate`)
      
      ws.onopen = () => {
        ws.send(JSON.stringify({ 
            project_id: currentProjectId,
            goal: fastGoal,
            blueprint: parsedBlueprint,
            agent_role: role,
            execution_mode: "fast",
            code_files: codeFiles // Pass existing files so backend can edit them
        }))
      }
      
      // We will reuse the same message handler for generation
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'token') {
          // Ignore architect tokens in fast mode
        } else if (data.type === 'agent_state') {
          setAgentState(prev => ({ ...prev, activeAgent: data.agent }))
        } else if (data.type === 'timeline') {
          setAgentState(prev => ({
            ...prev,
            timeline: [...prev.timeline, { title: data.title, reason: data.reason, status: data.status }]
          }))
        } else if (data.type === 'timeline_update') {
          setAgentState(prev => {
            const newTimeline = [...prev.timeline]
            if (newTimeline.length > 0) {
              newTimeline[newTimeline.length - 1].status = data.status
            }
            return { ...prev, timeline: newTimeline }
          })
        } else if (data.type === 'progress') {
          setLiveUpdates(prev => [...prev.slice(-4), data.message])
        } else if (data.type === 'file_created') {
          setCodeFiles(prev => ({ ...prev, [data.file]: data.content }))
        } else if (data.type === 'error') {
          setError(data.message)
          setIsLoading(false)
        } else if (data.type === 'done') {
          setIsLoading(false)
          setStep(3)
        }
      }
      
      ws.onerror = () => {
        setError("WebSocket connection failed")
        setIsLoading(false)
      }
      
      ws.onclose = () => {
        if (isLoading) setIsLoading(false)
      }
    } catch (err) {
      setError(err.message)
      setIsLoading(false)
    }
  }

  const handleGenerate = async (e) => {
    if (e && e.preventDefault) e.preventDefault();
    setIsLoading(true)
    setError(null)
    setLiveUpdates([])
    setAgentState({ activeAgent: 'architect', timeline: [] })
    setAwaitingApproval(false)
    setStep(3) // ⚡ INSTANT TRANSITION TO WORKSPACE & LIVE CODE STREAM
    setActiveWorkspaceTab('preview') // ⚡ FORCE ACTIVE TAB TO LIVE PREVIEW
    
    let parsedBlueprint;
    let rawJson = blueprintJson.trim();
    try {
        // Strip out any trailing markdown ticks and text before/after JSON
        rawJson = rawJson.replace(/```json/g, '').replace(/```/g, '').trim();
        const startIdx = rawJson.indexOf('{');
        const endIdx = rawJson.lastIndexOf('}');
        if (startIdx !== -1 && endIdx !== -1) rawJson = rawJson.substring(startIdx, endIdx + 1);
        
        // Strip trailing commas before closing braces/brackets (common LLM hallucination)
        rawJson = rawJson.replace(/,(?=\s*[}\]])/g, '');
        
        parsedBlueprint = JSON.parse(rawJson);
    } catch (e) {
        try {
            // Attempt auto-repair for truncated JSON arrays/objects
            if (rawJson.endsWith(',')) rawJson = rawJson.slice(0, -1);
            if (rawJson.endsWith('"')) rawJson += '"]}'; // cut off mid-string in file_structure
            else if (!rawJson.endsWith('}')) {
                if (rawJson.includes('"file_structure": [') && !rawJson.includes(']')) {
                    rawJson += ']}';
                } else {
                    rawJson += '}';
                }
            }
            // Strip trailing commas one last time just in case the repair added something weird
            rawJson = rawJson.replace(/,(?=\s*[}\]])/g, '');
            
            parsedBlueprint = JSON.parse(rawJson);
        } catch (repairError) {
            setError("Invalid JSON format in Blueprint! Scroll down and fix the missing brackets or trailing commas.");
            setIsLoading(false);
            return;
        }
    }

    try {
      const currentProjectId = projectId || `proj-${Math.random().toString(36).substr(2, 8)}`;
      if (!projectId) setProjectId(currentProjectId);
      
      const ws = new WebSocket(`${WS_URL}/api/ws/generate`)
      
      ws.onopen = () => {
        ws.send(JSON.stringify({ 
            project_id: currentProjectId,
            goal: goal,
            blueprint: parsedBlueprint,
            agent_role: agentRole
        }))
      }

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        
        if (data.type === "progress") {
          setLiveUpdates(prev => [...prev, data.message])
        } else if (data.type === "file_start") {
          setLiveUpdates(prev => [...prev, `Writing code for ${data.file}...`])
          setStreamFileName(data.file)
          streamFileNameRef.current = data.file;
          streamBufferRef.current = ""; // Reset buffer for new file
          setStreamedCode(""); // Reset UI state for new file
        } else if (data.type === "code_token") {
          // Push to JS buffer instead of React State to prevent 100hz re-renders
          if (data.file === streamFileNameRef.current) {
            streamBufferRef.current += data.token;
          }

        } else if (data.type === "code_complete") {
          // [ZERO-LATENCY] Instantly unlock the UI and show the Artifact Viewer!
          setCodeFiles(data.code_files)
          setStep(3)
          setIsLoading(false)
        } else if (data.type === "complete") {
          // The background executor has finished. Update any final logs.
          if (data.code_files) setCodeFiles(data.code_files)
          setExecutionLogs(data.execution_logs)
          setStep(3)
          setIsLoading(false)
          // Keep ws open to receive PREVIEW_READY
        } else if (data.type === "INTERRUPT") {
          // ⚡ AUTONOMOUS MODE: Always auto-approve, never show blueprint page again
          setAwaitingApproval(true)
          setTimeout(() => handleResume('approve'), 600);
        } else if (data.type === "PREVIEW_ERROR") {
          setAgentState(prev => ({ ...prev, activeAgent: 'error' }))
          setPreviewError(data.message)
          setIsBackend(true) // So ExecutionManager routes to BackendSandbox to show the error
          setIsPreviewRunning(true)
          ws.close()
        } else if (data.type === "PREVIEW_READY") {
          setAgentState(prev => ({ ...prev, activeAgent: 'ready' }))
          setPreviewError(null)
          if (data.isBackend) {
             setPreviewUrl(data.url);
             setIsBackend(true);
          } else {
             setPreviewUrl(null);
             setIsBackend(false);
          }
          setIsPreviewRunning(true)
          ws.close()
        } else if (data.type === "agent_state") {
          setAgentState(prev => ({ ...prev, activeAgent: data.agent }))
        } else if (data.type === "timeline") {
          setAgentState(prev => ({ 
            ...prev, 
            timeline: [...prev.timeline, { title: data.title, reason: data.reason, status: data.status }] 
          }))
        } else if (data.type === "timeline_update") {
          setAgentState(prev => {
            const newTimeline = [...prev.timeline];
            if (newTimeline.length > 0) {
               newTimeline[newTimeline.length - 1].status = data.status;
            }
            return { ...prev, timeline: newTimeline };
          });
        } else if (data.type === "error") {
          setError(data.message)
          setIsLoading(false)
          ws.close()
        }
      }

      ws.onerror = (e) => {
        console.error('WebSocket error:', e)
        setError("⚠️ Connection lost during build. Click Retry to continue.")
        setIsLoading(false)
        // Stay on step 2 (generation view) — do NOT bounce to home or blueprint
      }

      ws.onclose = (e) => {
        if (e.code !== 1000 && isLoading) {
          setError("⚠️ Build interrupted. Click Retry below.")
          setIsLoading(false)
        }
      }
    } catch (err) {
      setError(err.message)
      setIsLoading(false)
      setStep(1)
    }
  }

  const handleResume = async (action) => {
    setAwaitingApproval(false)
    try {
        const response = await fetch(`${API_URL}/api/resume_generation`, {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${session?.access_token || 'mock-token-for-local-dev'}`
            },
            body: JSON.stringify({ project_id: projectId, action })
        });
        
        const data = await response.json();
        if (data.status === "aborted") {
            setError("Deployment aborted by user.");
            setIsLoading(false);
            setStep(1);
        } else {
            setLiveUpdates(prev => [...prev, "▶️ Resuming deployment..."]);
        }
    } catch (err) {
        setError(err.message);
        setAwaitingApproval(false);
    }
  }

  if (!session) {
    return <Auth />
  }

  return (
    <div className="app-container" style={{ display: 'flex', flexDirection: 'column', height: '100dvh', backgroundColor: 'var(--app-bg)', color: 'var(--text-primary)', overflow: 'hidden' }}>
      
      {/* TOP NAV BAR */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 24px', backgroundColor: 'var(--sidebar-bg)', borderBottom: '1px solid var(--border-color)', zIndex: 10 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button onClick={() => setShowSidebar(!showSidebar)} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', fontSize: '1.4rem', cursor: 'pointer', padding: '2px 4px', display: 'flex', alignItems: 'center', justifyContent: 'center' }} title="Toggle Sidebar">
            ☰
          </button>
          <img src={prismaiLogo} alt="PrismAI Logo" style={{ width: '34px', height: '34px', objectFit: 'contain', display: 'block', marginLeft: '2px' }} />
          <h1 style={{ margin: 0, fontSize: '1.2rem', letterSpacing: '0.5px', fontWeight: '600', marginLeft: '2px' }}>PrismAI</h1>
          <span style={{ 
            fontSize: '0.75rem', 
            fontWeight: 'bold', 
            padding: '3px 8px', 
            borderRadius: '6px', 
            textTransform: 'uppercase',
            backgroundColor: userTier === 'pro' ? 'rgba(168, 85, 247, 0.2)' : userTier === 'plus' ? 'rgba(59, 130, 246, 0.2)' : userTier === 'go' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(255, 255, 255, 0.1)',
            color: userTier === 'pro' ? '#c084fc' : userTier === 'plus' ? '#60a5fa' : userTier === 'go' ? '#4ade80' : '#94a3b8',
            border: `1px solid ${userTier === 'pro' ? '#a855f7' : userTier === 'plus' ? '#3b82f6' : userTier === 'go' ? '#22c55e' : '#475569'}`
          }}>
            {userTier === 'pro' ? '👑 PRO' : userTier === 'plus' ? '⚡ PLUS' : userTier === 'go' ? '🚀 GO' : 'FREE'}
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button 
            onClick={handleShareChat} 
            style={{ 
              backgroundColor: 'rgba(168, 85, 247, 0.1)', 
              border: '1px solid rgba(168, 85, 247, 0.3)', 
              color: '#c084fc', 
              padding: '6px 14px', 
              borderRadius: '20px', 
              fontSize: '0.85rem', 
              fontWeight: '500', 
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.2s ease',
              backdropFilter: 'blur(4px)'
            }}
            title="Share this Chat Thread"
          >
            🔗 Share
          </button>
          <button 
            onClick={() => setShowUpgradeModal(true)} 
            style={{ 
              backgroundColor: 'rgba(59, 130, 246, 0.08)', 
              border: '1px solid rgba(59, 130, 246, 0.25)', 
              color: '#93c5fd', 
              padding: '6px 14px', 
              borderRadius: '20px', 
              fontSize: '0.85rem', 
              fontWeight: '500', 
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.2s ease',
              backdropFilter: 'blur(4px)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.18)';
              e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.45)';
              e.currentTarget.style.color = '#bfdbfe';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.08)';
              e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.25)';
              e.currentTarget.style.color = '#93c5fd';
            }}
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z"/>
            </svg>
            <span>Upgrade</span>
          </button>
        </div>
      </header>

      {/* UPGRADE PRICING MODAL (ChatGPT Killer Matrix) */}
      {showUpgradeModal && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', zIndex: 9999, display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '20px' }}>
          <div style={{ backgroundColor: '#101216', border: '1px solid #2a2d36', borderRadius: '20px', maxWidth: '1050px', width: '100%', padding: '32px', position: 'relative', boxShadow: '0 25px 60px rgba(0,0,0,0.9)' }}>
            <button onClick={() => setShowUpgradeModal(false)} style={{ position: 'absolute', top: '20px', right: '20px', background: 'none', border: 'none', color: '#888', fontSize: '1.5rem', cursor: 'pointer' }}>✕</button>
            <div style={{ textAlign: 'center', marginBottom: '28px' }}>
              <h2 style={{ fontSize: '2rem', fontWeight: '800', margin: '0 0 8px 0', background: 'linear-gradient(135deg, #60a5fa, #c084fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Choose Your PrismAI Plan</h2>
              <p style={{ color: '#94a3b8', margin: 0, fontSize: '0.95rem' }}>Select the optimal power tier for your AI engineering, live compilation, and multi-agent workflows.</p>
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: '16px' }}>
              {/* FREE TIER */}
              <div style={{ backgroundColor: '#16181d', border: '1px solid #262930', borderRadius: '14px', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <h3 style={{ margin: '0 0 4px 0', fontSize: '1.15rem', color: '#e0e0e0' }}>Free</h3>
                  <p style={{ fontSize: '0.75rem', color: '#64748b', margin: '0 0 12px 0' }}>Essential AI capabilities</p>
                  <div style={{ fontSize: '1.6rem', fontWeight: 'bold', margin: '8px 0', color: '#fff' }}>₹0 <span style={{ fontSize: '0.8rem', color: '#888' }}>/ month</span></div>
                  <ul style={{ paddingLeft: '16px', margin: '14px 0', color: '#94a3b8', fontSize: '0.8rem', lineHeight: '1.7' }}>
                    <li>30 Queries / day</li>
                    <li>Sub-150ms Instant Model</li>
                    <li>1 Active Project</li>
                    <li>Basic WASM Preview</li>
                  </ul>
                </div>
                <button onClick={() => handleUpgradeTier('free')} disabled={userTier === 'free'} style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #333', backgroundColor: userTier === 'free' ? '#222' : '#333', color: userTier === 'free' ? '#666' : '#fff', cursor: userTier === 'free' ? 'default' : 'pointer' }}>
                  {userTier === 'free' ? 'Current Plan' : 'Downgrade to Free'}
                </button>
              </div>

              {/* GO TIER */}
              <div style={{ backgroundColor: '#132219', border: '1px solid #22c55e', borderRadius: '14px', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <h3 style={{ margin: '0 0 4px 0', fontSize: '1.15rem', color: '#4ade80' }}>🚀 Go</h3>
                  <p style={{ fontSize: '0.75rem', color: '#64748b', margin: '0 0 12px 0' }}>Expanded access & 3D WebGL</p>
                  <div style={{ fontSize: '1.6rem', fontWeight: 'bold', margin: '8px 0', color: '#fff' }}>₹299 <span style={{ fontSize: '0.8rem', color: '#888' }}>/ month</span></div>
                  <ul style={{ paddingLeft: '16px', margin: '14px 0', color: '#bbf7d0', fontSize: '0.8rem', lineHeight: '1.7' }}>
                    <li>150 Queries / day</li>
                    <li>3D WebGL Engine ✅</li>
                    <li>Voice AI Integration</li>
                    <li>100k Context Memory</li>
                    <li>5 Active Projects</li>
                  </ul>
                </div>
                <button onClick={() => handleUpgradeTier('go')} style={{ width: '100%', padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: '#22c55e', color: '#fff', fontWeight: 'bold', cursor: 'pointer' }}>
                  {userTier === 'go' ? 'Current Plan' : 'Upgrade to Go 🚀'}
                </button>
              </div>

              {/* PLUS TIER */}
              <div style={{ backgroundColor: '#131e33', border: '2px solid #3b82f6', borderRadius: '14px', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', position: 'relative' }}>
                <div style={{ position: 'absolute', top: '-10px', right: '14px', backgroundColor: '#3b82f6', color: '#fff', fontSize: '0.65rem', fontWeight: 'bold', padding: '2px 8px', borderRadius: '10px' }}>POPULAR</div>
                <div>
                  <h3 style={{ margin: '0 0 4px 0', fontSize: '1.15rem', color: '#60a5fa' }}>⚡ Plus</h3>
                  <p style={{ fontSize: '0.75rem', color: '#64748b', margin: '0 0 12px 0' }}>Full 37-Agent Swarm & IDE</p>
                  <div style={{ fontSize: '1.6rem', fontWeight: 'bold', margin: '8px 0', color: '#fff' }}>₹1,499 <span style={{ fontSize: '0.8rem', color: '#888' }}>/ month</span></div>
                  <ul style={{ paddingLeft: '16px', margin: '14px 0', color: '#cbd5e1', fontSize: '0.8rem', lineHeight: '1.7' }}>
                    <li>1,000 Queries / day</li>
                    <li>Full 37-Agent Swarm Matrix</li>
                    <li>In-Browser WebContainer IDE</li>
                    <li>Self-Healing Code Interceptor</li>
                    <li>30-Day Vector Memory</li>
                  </ul>
                </div>
                <button onClick={() => handleUpgradeTier('plus')} style={{ width: '100%', padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: '#3b82f6', color: '#fff', fontWeight: 'bold', cursor: 'pointer' }}>
                  {userTier === 'plus' ? 'Current Plan' : 'Upgrade to Plus ⚡'}
                </button>
              </div>

              {/* PRO TIER */}
              <div style={{ backgroundColor: '#211430', border: '2px solid #a855f7', borderRadius: '14px', padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <h3 style={{ margin: '0 0 4px 0', fontSize: '1.15rem', color: '#c084fc' }}>👑 Pro</h3>
                  <p style={{ fontSize: '0.75rem', color: '#64748b', margin: '0 0 12px 0' }}>Air-gapped executive suite</p>
                  <div style={{ fontSize: '1.6rem', fontWeight: 'bold', margin: '8px 0', color: '#fff' }}>₹7,999 <span style={{ fontSize: '0.8rem', color: '#888' }}>/ month</span></div>
                  <ul style={{ paddingLeft: '16px', margin: '14px 0', color: '#e9d5ff', fontSize: '0.8rem', lineHeight: '1.7' }}>
                    <li>Unlimited Queries</li>
                    <li>100% Air-Gapped Privacy</li>
                    <li>Docker Sandbox Execution</li>
                    <li>Unlimited Swarm Rollouts</li>
                    <li>Permanent AST Memory</li>
                  </ul>
                </div>
                <button onClick={() => handleUpgradeTier('pro')} style={{ width: '100%', padding: '10px', borderRadius: '8px', border: 'none', backgroundColor: '#a855f7', color: '#fff', fontWeight: 'bold', cursor: 'pointer' }}>
                  {userTier === 'pro' ? 'Current Plan' : 'Upgrade to Pro 👑'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* MAIN CONTENT AREA */}
      <div className="main-content-wrapper" style={{ display: 'flex', flex: 1, overflow: 'hidden', position: 'relative' }}>
        
        {activeView === 'dashboards' ? (
           <div style={{ flex: 1, width: '100%', backgroundColor: 'var(--app-bg)' }}>
              <PlatformDashboards API_URL={API_URL} />
           </div>
        ) : (
           <>
        {/* LEFT NAVIGATION SIDEBAR */}
        {showSidebar && (
        <aside className="sidebar">
          {/* Header */}
          <div className="sidebar-header" style={{ justifyContent: 'flex-end' }}>
            <div className="sidebar-header-icon" onClick={() => setShowSidebar(false)} title="Close sidebar">
              <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="18" width="18" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line></svg>
            </div>
          </div>

          {/* New Chat Button */}
          <button className="sidebar-new-chat-btn" onClick={handleNewChat}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div className="sidebar-header-icon" style={{ width: '24px', height: '24px', background: 'white', color: 'black', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="14" width="14" xmlns="http://www.w3.org/2000/svg"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
              </div>
              <span>New chat</span>
            </div>
            <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="16" width="16" xmlns="http://www.w3.org/2000/svg"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
          </button>

          {/* Navigation Group */}
          <div className="sidebar-nav-group">
            <a href="#" className="sidebar-nav-item" onClick={(e) => { e.preventDefault(); alert("Coming soon!"); }}>
              <div className="sidebar-nav-icon">🔍</div>
              <span>Search chats</span>
            </a>

          </div>
          
          {/* History */}
          <div className="sidebar-history-title">Recents</div>
          <div className="sidebar-history-list">
            {chatHistoryList.map(chat => (
              <div 
                key={chat.id} 
                className={`sidebar-history-item ${currentChatId === chat.id ? 'active' : ''}`}
                onClick={() => handleLoadChat(chat.id)}
                title={chat.title}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden', flex: 1 }}>
                    <span className="history-item-text">{chat.title}</span>
                </div>
                <div className="history-actions" style={{ display: 'flex', gap: '6px' }}>
                    <button onClick={(e) => handleRenameChat(chat.id, e)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', opacity: 0.7, color: '#fff' }} title="Rename">✏️</button>
                    <button onClick={(e) => handleDeleteChat(chat.id, e)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', opacity: 0.7, color: '#fff' }} title="Delete">🗑️</button>
                </div>
              </div>
            ))}
          </div>
          
          {/* Footer User Profile & Actions */}
          <div className="sidebar-footer" style={{ marginTop: 'auto', paddingTop: '12px', borderTop: '1px solid rgba(255,255,255,0.05)', borderRadius: 0, padding: '12px 0 0 0' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px', borderRadius: '8px', width: '100%' }} >
              <div className="sidebar-user-info" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div className="sidebar-avatar" style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: '#3b82f6', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem', fontWeight: '600' }}>
                  {session?.user?.email?.[0]?.toUpperCase() || 'U'}
                </div>
                <div className="sidebar-user-details" style={{ display: 'flex', flexDirection: 'column' }}>
                  <span className="sidebar-user-name" style={{ color: '#ececec', fontSize: '0.9rem', fontWeight: '500' }}>{session?.user?.email?.split('@')[0] || 'Guest'}</span>
                  <span className="sidebar-user-plan" style={{ color: '#60a5fa', fontSize: '0.75rem', fontWeight: '600', letterSpacing: '0.5px' }}>PrismAI 2.0</span>
                </div>
              </div>
              
              <div style={{ display: 'flex', gap: '4px' }}>
                <button 
                  onClick={(e) => { e.stopPropagation(); setShowSettingsModal(true); }} 
                  className="sidebar-action-btn"
                  title="Settings"
                >
                  <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="16" width="16" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                </button>
                {session ? (
                  <button 
                    onClick={(e) => { e.stopPropagation(); supabase.auth.signOut(); }} 
                    className="sidebar-action-btn"
                    title="Sign Out"
                  >
                    <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="16" width="16" xmlns="http://www.w3.org/2000/svg"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                  </button>
                ) : (
                  <button 
                    onClick={(e) => { e.stopPropagation(); alert("Sign in from main view"); }} 
                    className="sidebar-action-btn"
                    title="Sign In"
                  >
                    <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="16" width="16" xmlns="http://www.w3.org/2000/svg"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>
                  </button>
                )}
              </div>
            </div>
          </div>
        </aside>
        )}

        {/* CHAT SECTION (Centers when step=1, shrinks to 30% when step>1) */}
        <div className="chat-section" style={{ 
          flex: step === 1 ? '1' : '0 0 35%', 
          minHeight: 0,
          maxWidth: step === 1 ? '100%' : '450px',
          display: 'flex', 
          flexDirection: 'column', 
          transition: 'all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)',
          borderRight: step === 1 ? 'none' : '1px solid #2a2a2a',
          position: 'relative'
        }}>
          
          <div style={{ flex: 1, overflowY: 'auto', padding: '20px 20px 120px 20px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ width: '100%', maxWidth: '800px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
              
              {chatMessages.length === 0 && step === 1 && (
                <div style={{ textAlign: 'center', marginTop: '18vh', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <h2 style={{ fontSize: '2.2rem', marginBottom: '8px', fontWeight: '600', color: '#f1f5f9', letterSpacing: '-0.5px' }}>
                    Where should we begin?
                  </h2>
                </div>
              )}

              {chatMessages.map((msg, idx) => (
                <div key={idx} className="chat-message-container" style={{ 
                  display: 'flex', 
                  gap: '16px', 
                  alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  maxWidth: '85%',
                  flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
                }}>
                  <div style={{ 
                    width: '32px', height: '32px', borderRadius: '50%', flexShrink: 0,
                    backgroundColor: msg.role === 'user' ? 'var(--border-color)' : 'var(--accent)',
                    display: 'flex', justifyContent: 'center', alignItems: 'center', fontSize: '14px',
                    textTransform: 'uppercase'
                  }}>
                    {msg.role === 'user' ? (session?.user?.email?.[0] || 'U') : 'A'}
                  </div>
                  <div style={{ 
                    backgroundColor: msg.role === 'user' ? 'var(--border-color)' : 'transparent',
                    padding: msg.role === 'user' ? '12px 18px' : '6px 0',
                    borderRadius: '16px',
                    borderTopRightRadius: msg.role === 'user' ? '4px' : '16px',
                    borderTopLeftRadius: msg.role === 'ai' ? '4px' : '16px',
                    lineHeight: '1.6',
                    fontSize: '1rem',
                    color: '#e0e0e0',
                    position: 'relative'
                  }}>
                    {msg.image && (
                      <div style={{ marginBottom: '10px' }}>
                        <img src={msg.image} alt="Uploaded" style={{ maxWidth: '300px', maxHeight: '300px', borderRadius: '8px', border: '1px solid #444', objectFit: 'contain' }} />
                      </div>
                    )}
                    {msg.visuals && msg.visuals.length > 0 && (
                      <div style={{ 
                          display: 'grid', 
                          gridTemplateColumns: msg.visuals.length > 1 ? 'repeat(auto-fit, minmax(200px, 1fr))' : '1fr', 
                          gap: '12px', 
                          marginBottom: '16px', 
                          width: '100%',
                          maxWidth: '600px'
                      }}>
                        {msg.visuals.filter(v => v.media_type === 'image').map((v, i) => (
                          <div key={i} style={{ borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--border-color)', boxShadow: '0 4px 20px rgba(0,0,0,0.2)' }}>
                            <img src={v.url} alt={v.alt || 'Visual'} style={{ width: '100%', height: '100%', maxHeight: msg.visuals.length > 1 ? '200px' : '300px', objectFit: 'cover', display: 'block' }} />
                          </div>
                        ))}
                      </div>
                    )}
                    {console.log("RENDERING MSG CONTENT:", msg.content)}
                    {renderMessageContent(msg.content + (idx === chatMessages.length - 1 && isChatLoading && msg.role === 'ai' ? ' ▋' : ''), (jsonStr) => { setActiveArchitecture(jsonStr); setStep(4); setActiveWorkspaceTab('architecture'); })}
                    {msg.role === 'ai' && (
                      <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
                        <button 
                          onClick={() => handleCopy(idx, msg.content)} 
                          style={{ background: 'none', border: 'none', cursor: 'pointer', opacity: copiedIndex === idx ? 1 : 0.6, fontSize: '0.9rem', transition: 'opacity 0.2s' }}
                          title="Copy response"
                        >
                          {copiedIndex === idx ? '✅' : '📋'}
                        </button>
                        <button 
                          onClick={() => handleFeedback(idx, 'up')} 
                          style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '0.9rem', transition: 'all 0.2s', opacity: feedbackState[idx] === 'up' ? 1 : 0.6, filter: feedbackState[idx] === 'up' ? 'drop-shadow(0 0 5px #4ade80)' : 'none' }}
                          title="Good response"
                        >
                          👍
                        </button>
                        <button 
                          onClick={() => handleFeedback(idx, 'down')} 
                          style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '0.9rem', transition: 'all 0.2s', opacity: feedbackState[idx] === 'down' ? 1 : 0.6, filter: feedbackState[idx] === 'down' ? 'drop-shadow(0 0 5px #f87171)' : 'none' }}
                          title="Bad response"
                        >
                          👎
                        </button>
                      </div>
                    )}
                  </div>
                  {msg.role === 'user' && (
                    <button 
                      onClick={() => handleEditMessage(idx)}
                      style={{
                        background: 'none', border: 'none', color: 'var(--modal-text-color)', cursor: 'pointer',
                        fontSize: '0.9rem', padding: '0 8px', alignSelf: 'center', opacity: 0.7
                      }}
                      title="Edit this message"
                      onMouseEnter={(e) => e.currentTarget.style.opacity = 1}
                      onMouseLeave={(e) => e.currentTarget.style.opacity = 0.7}
                    >
                      ✏️
                    </button>
                  )}
                </div>
              ))}
              
              {isChatLoading && (
                <div style={{ display: 'flex', gap: '16px', alignSelf: 'flex-start' }}>
                   <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: 'var(--accent)', display: 'flex', justifyContent: 'center', alignItems: 'center', color: '#fff', fontWeight: 'bold' }}>A</div>
                   <div style={{ padding: '6px 0', display: 'flex', alignItems: 'center', gap: '12px' }}>
                     <div className="spinner" style={{ width: '18px', height: '18px' }}></div>
                     {chatStatus && (
                         <span style={{ fontSize: '0.9rem', color: '#9ca3af', fontStyle: 'italic', animation: 'pulse 2s infinite' }}>{chatStatus}</span>
                     )}
                   </div>
                </div>
              )}
              
              {/* Add padding at the bottom so the last message isn't hidden behind the input */}
              <div ref={chatEndRef} style={{ height: '20px' }}></div>
            </div>
          </div>
          
          {/* FLOATING INPUT BOX */}
          <div style={{ 
            position: 'absolute', 
            bottom: '20px', 
            left: '0', 
            right: '0', 
            display: 'flex', 
            flexDirection: 'column',
            alignItems: 'center',
            padding: '0 20px'
          }}>
            {/* Image Preview Thumbnail */}
            {selectedImages.length > 0 && (
              <div style={{
                position: 'relative',
                marginBottom: '10px',
                width: '100%',
                maxWidth: '800px',
                display: 'flex',
                gap: '12px',
                overflowX: 'auto',
                padding: '4px 0'
              }}>
                {selectedImages.map((img, idx) => (
                  <div key={idx} style={{ position: 'relative', display: 'inline-block' }}>
                    <img src={img} alt={`Upload preview ${idx}`} style={{ height: '60px', borderRadius: '8px', border: '2px solid #444', objectFit: 'cover' }} />
                    <button 
                      type="button"
                      onClick={() => setSelectedImages(prev => prev.filter((_, i) => i !== idx))} 
                      style={{ position: 'absolute', top: '-8px', right: '-8px', background: '#ef4444', color: 'white', border: 'none', borderRadius: '50%', width: '22px', height: '22px', fontSize: '14px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 2px 5px rgba(0,0,0,0.3)' }}
                    >×</button>
                  </div>
                ))}
              </div>
            )}
            


            <form onSubmit={handleChatSubmit} style={{ 
              width: '100%', 
              maxWidth: '800px', 
              backgroundColor: 'var(--btn-bg)', 
              borderRadius: '24px', 
              padding: '8px', 
              display: 'flex', 
              alignItems: 'center', 
              border: '1px solid var(--border-color)',
              boxShadow: '0 10px 30px rgba(0,0,0,0.5)'
            }}>
              <input type="file" multiple accept="image/*" ref={fileInputRef} onChange={handleImageUpload} style={{ display: 'none' }} />
              <button 
                type="button" 
                onClick={() => fileInputRef.current?.click()}
                style={{
                  background: 'none', 
                  border: 'none', 
                  color: 'var(--modal-text-color)',
                  fontSize: '1.4rem', 
                  cursor: 'pointer', 
                  padding: '0 12px', 
                  transition: 'color 0.2s',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
                title="Attach Image"
                onMouseEnter={(e) => e.target.style.color = '#fff'}
                onMouseLeave={(e) => e.target.style.color = '#888'}
              >
                +
              </button>
              <input 
                type="text" 
                value={chatInput} 
                onChange={(e) => setChatInput(e.target.value)} 
                placeholder={step === 1 ? "Message PrismAI..." : "Update your app..."} 
                style={{ 
                  flex: 1, 
                  minWidth: 0,
                  padding: '12px 20px', 
                  backgroundColor: 'transparent', 
                  border: 'none', 
                  color: 'var(--text-primary)', 
                  fontSize: '1rem', 
                  outline: 'none' 
                }}
              />
              <button
                type="button"
                onClick={startVoiceRecognition}
                style={{
                  background: 'none', 
                  border: 'none', 
                  color: isRecording ? '#ef4444' : '#888',
                  cursor: 'pointer', 
                  padding: '0 10px', 
                  transition: 'all 0.2s',
                  transform: isRecording ? 'scale(1.05)' : 'scale(1)'
                }}
                title={isRecording ? "Listening..." : "Voice Input"}
              >
                {isRecording ? (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(239, 68, 68, 0.1)', padding: '6px 12px', borderRadius: '20px', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
                        <span style={{ fontSize: '1rem', animation: 'pulse 1.5s infinite' }}>🔴</span>
                        <span style={{ fontSize: '0.8rem', fontWeight: '600', color: '#ef4444' }}>Listening</span>
                    </div>
                ) : (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(59, 130, 246, 0.1)', padding: '6px 12px', borderRadius: '20px', border: '1px solid rgba(59, 130, 246, 0.3)', transition: 'all 0.3s', boxShadow: '0 0 10px rgba(59, 130, 246, 0.1)' }} onMouseEnter={(e) => { e.currentTarget.style.background = 'rgba(59, 130, 246, 0.2)'; e.currentTarget.style.boxShadow = '0 0 15px rgba(59, 130, 246, 0.3)'; }} onMouseLeave={(e) => { e.currentTarget.style.background = 'rgba(59, 130, 246, 0.1)'; e.currentTarget.style.boxShadow = '0 0 10px rgba(59, 130, 246, 0.1)'; }}>
                        <span style={{ fontSize: '1rem' }}>✨</span>
                        <span style={{ fontSize: '0.8rem', fontWeight: '600', color: '#60a5fa', letterSpacing: '0.5px' }}>Voice AI</span>
                    </div>
                )}
              </button>
              
              <button
                type="button"
                onClick={() => setIsWebSearchEnabled(!isWebSearchEnabled)}
                style={{
                  background: 'none', 
                  border: 'none', 
                  color: isWebSearchEnabled ? '#10b981' : '#888',
                  cursor: 'pointer', 
                  padding: '0 10px', 
                  transition: 'all 0.2s',
                  transform: isWebSearchEnabled ? 'scale(1.05)' : 'scale(1)'
                }}
                title={isWebSearchEnabled ? "Web Search Enabled" : "Web Search"}
              >
                {isWebSearchEnabled ? (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(16, 185, 129, 0.1)', padding: '6px 12px', borderRadius: '20px', border: '1px solid rgba(16, 185, 129, 0.3)', boxShadow: '0 0 10px rgba(16, 185, 129, 0.1)' }}>
                        <span style={{ fontSize: '1rem' }}>🌐</span>
                        <span style={{ fontSize: '0.8rem', fontWeight: '600', color: '#10b981', letterSpacing: '0.5px' }}>Search ON</span>
                    </div>
                ) : (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(136, 136, 136, 0.1)', padding: '6px 12px', borderRadius: '20px', border: '1px solid rgba(136, 136, 136, 0.3)', transition: 'all 0.3s' }} onMouseEnter={(e) => { e.currentTarget.style.background = 'rgba(136, 136, 136, 0.2)'; }} onMouseLeave={(e) => { e.currentTarget.style.background = 'rgba(136, 136, 136, 0.1)'; }}>
                        <span style={{ fontSize: '1rem', opacity: 0.7 }}>🌐</span>
                        <span style={{ fontSize: '0.8rem', fontWeight: '600', color: '#888', letterSpacing: '0.5px' }}>Search</span>
                    </div>
                )}
              </button>
              <button 
                type="submit" 
                disabled={isChatLoading || !chatInput.trim()} 
                style={{ 
                  width: '40px', 
                  height: '40px', 
                  borderRadius: '50%', 
                  backgroundColor: (isChatLoading || !chatInput.trim()) ? 'var(--border-color)' : 'var(--accent)', 
                  border: 'none', 
                  color: 'var(--text-primary)', 
                  display: 'flex', 
                  justifyContent: 'center', 
                  alignItems: 'center', 
                  cursor: (isChatLoading || !chatInput.trim()) ? 'not-allowed' : 'pointer',
                  transition: 'background 0.2s'
                }}
              >
                ➤
              </button>
            </form>
          </div>
        </div>

        {/* WORKSPACE PANEL (Hidden in step 1, takes remaining width in step 2 & 3) */}
        {step > 1 && (
          <div className="preview-section" style={{ flex: 1, minHeight: 0, backgroundColor: '#0a0a0a', display: 'flex', flexDirection: 'column', position: 'relative' }}>
            
            {/* WORKSPACE CONTENT */}
            <div style={{ flex: 1, overflowY: 'auto', padding: '30px' }}>
              
              {/* STEP 2: REVIEW BLUEPRINT */}
              {step === 2 && (
                <div style={{ animation: 'fadeIn 0.5s ease-out' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                    <h2 style={{ margin: 0, fontWeight: '500' }}>Architect's Blueprint</h2>
                    <button onClick={handleGenerate} disabled={isLoading} style={{ padding: '10px 20px', borderRadius: '8px', backgroundColor: 'var(--accent)', color: 'var(--text-primary)', border: 'none', fontWeight: 'bold', cursor: isLoading ? 'not-allowed' : 'pointer' }}>
                      {isLoading ? 'Generating Code...' : 'Approve & Build'}
                    </button>
                  </div>
                  <p style={{ color: 'var(--modal-text-color)', marginBottom: '20px' }}>Review the proposed architecture below. You can edit the JSON directly before building.</p>
                  
                  <textarea 
                      style={{ width: '100%', height: 'calc(100dvh - 250px)', backgroundColor: '#1e1e1e', color: '#00ff00', padding: '20px', fontFamily: 'monospace', borderRadius: '12px', border: '1px solid var(--border-color)', resize: 'none', outline: 'none' }}
                      value={blueprintJson}
                      onChange={(e) => setBlueprintJson(e.target.value)}
                      disabled={isLoading}
                  />
                </div>
              )}

              {/* STEP 1: WELCOME SCREEN */}
              {step === 1 && !isLoading && (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh', color: 'var(--text-secondary)' }}>
                  <div style={{ fontSize: '4rem', marginBottom: '20px' }}>🤖</div>
                  <h2>Welcome to the Omni-Chat Builder</h2>
                  <p>Talk to PrismAI Advisor on the left.</p>
                  <p>Ask questions, or ask it to "build a new project" and watch the magic happen!</p>
                </div>
              )}

              {/* UNIFIED OS WORKSPACE (Combines Code, Preview, Logs, Architecture) */}
              {(step === 3 || step === 4) && (
                <div style={{ height: 'calc(100dvh - 60px)', animation: 'fadeIn 0.5s ease-out', margin: '-30px', position: 'relative' }}>
                  <AIWorkspaceTabs 
                    activeTab={activeWorkspaceTab}
                    setActiveTab={setActiveWorkspaceTab}
                    codeFiles={codeFiles}
                    setCodeFiles={setCodeFiles}
                    blueprintJson={activeArchitecture ? activeArchitecture : blueprintJson}
                    executionLogs={executionLogs}
                    previewUrl={previewUrl}
                    previewError={previewError}
                    isBackend={isBackend}
                    projectId={projectId}
                    isPreviewRunning={isPreviewRunning}
                    previewPort={previewPort}
                    API_URL={API_URL}
                    timeline={agentState.timeline}
                  />
                  {/* 🚀 ONE-CLICK DOWNLOAD BUTTON */}
                  {projectId && (
                    <a
                      href={`${API_URL}/api/download/${projectId}`}
                      download
                      style={{
                        position: 'absolute',
                        bottom: '24px',
                        right: '24px',
                        zIndex: 100,
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '12px 22px',
                        background: 'linear-gradient(135deg, #10b981, #059669)',
                        color: '#fff',
                        borderRadius: '50px',
                        fontWeight: '700',
                        fontSize: '0.95rem',
                        textDecoration: 'none',
                        boxShadow: '0 4px 20px rgba(16,185,129,0.45)',
                        transition: 'all 0.2s',
                        letterSpacing: '0.3px'
                      }}
                      onMouseEnter={e => { e.currentTarget.style.transform = 'scale(1.05)'; e.currentTarget.style.boxShadow = '0 6px 28px rgba(16,185,129,0.6)'; }}
                      onMouseLeave={e => { e.currentTarget.style.transform = 'scale(1)'; e.currentTarget.style.boxShadow = '0 4px 20px rgba(16,185,129,0.45)'; }}
                    >
                      <span style={{ fontSize: '1.2rem' }}>⬇️</span>
                      Download &amp; Run
                    </a>
                  )}
                </div>
              )}

              
              {/* LIVE PROGRESS DASHBOARD OVERLAY for Workspace */}
              {isLoading && step === 2 && (
                <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(10,10,10,0.95)', display: 'flex', flexDirection: 'column', zIndex: 50, padding: '30px', animation: 'fadeIn 0.3s ease-out' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                     <h3 style={{ margin: 0, fontWeight: '500', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        {awaitingApproval ? (
                           <div style={{ width: '20px', height: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>⏸️</div>
                        ) : (
                           <div className="spinner" style={{ width: '20px', height: '20px' }}></div>
                        )}
                        {awaitingApproval ? 'Paused for Approval' : 'PrismAI is engineering your application...'}
                     </h3>
                     <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                       {awaitingApproval && (
                          <div style={{ display: 'flex', gap: '10px' }}>
                             <button 
                               onClick={() => handleResume('approve')}
                               style={{ padding: '6px 12px', backgroundColor: 'var(--accent-color)', color: 'white', border: 'none', borderRadius: '6px', fontWeight: '500', cursor: 'pointer', fontSize: '0.85rem' }}>
                               Approve
                             </button>
                             <button 
                               onClick={() => handleResume('abort')}
                               style={{ padding: '6px 12px', backgroundColor: 'transparent', color: 'var(--modal-text-color)', border: '1px solid var(--border-color)', borderRadius: '6px', fontWeight: '500', cursor: 'pointer', fontSize: '0.85rem' }}>
                               Abort
                             </button>
                          </div>
                       )}
                     </div>
                  </div>
                  
                  {/* Dashboard Component */}
                  <ProgressDashboard 
                     activeAgent={agentState.activeAgent} 
                     timeline={agentState.timeline} 
                     liveUpdates={liveUpdates} 
                     streamFileName={streamFileName}
                     streamedCode={streamedCode}
                  />

                  {/* ⚠️ ERROR BANNER WITH RETRY — shown when build crashes */}
                  {error && (
                    <div style={{
                      position: 'absolute', bottom: '30px', left: '30px', right: '30px',
                      background: 'linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05))',
                      border: '1px solid rgba(239,68,68,0.4)', borderRadius: '12px',
                      padding: '16px 20px', display: 'flex', alignItems: 'center',
                      justifyContent: 'space-between', gap: '16px', zIndex: 200,
                      backdropFilter: 'blur(10px)'
                    }}>
                      <span style={{ color: '#fca5a5', fontSize: '0.9rem', flex: 1 }}>
                        {error}
                      </span>
                      <button
                        onClick={() => { setError(null); handleGenerate(); }}
                        style={{
                          padding: '8px 20px', background: 'linear-gradient(135deg, #f97316, #ea580c)',
                          color: '#fff', border: 'none', borderRadius: '8px',
                          fontWeight: '700', cursor: 'pointer', fontSize: '0.9rem',
                          whiteSpace: 'nowrap', flexShrink: 0
                        }}
                      >
                        🔄 Retry Build
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
           </>
        )}
        
        {/* SETTINGS MODAL */}
        {showSettingsModal && (
          <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'var(--modal-overlay)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 999 }}>
            <div style={{ backgroundColor: 'var(--sidebar-bg)', padding: '30px', borderRadius: '16px', width: '90%', maxWidth: '400px', border: '1px solid var(--border-color)', boxShadow: '0 20px 40px rgba(0,0,0,0.5)' }}>
              <h2 style={{ margin: '0 0 20px 0', fontSize: '1.5rem', fontWeight: '600' }}>Settings</h2>
              
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', color: 'var(--modal-text-color)', marginBottom: '8px', fontSize: '0.9rem' }}>Account Email</label>
                <div style={{ padding: '12px', backgroundColor: 'var(--input-bg)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-secondary)' }}>
                  {session?.user?.email}
                </div>
              </div>
              


              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
                <button onClick={() => setShowSettingsModal(false)} style={{ padding: '10px 20px', backgroundColor: 'var(--accent)', color: 'var(--text-primary)', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
                  Save & Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* SHARE CHAT MODAL */}
        {showShareModal && (
          <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.75)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000, backdropFilter: 'blur(8px)' }}>
            <div style={{ backgroundColor: 'var(--sidebar-bg)', padding: '28px', borderRadius: '18px', width: '90%', maxWidth: '480px', border: '1px solid rgba(168, 85, 247, 0.4)', boxShadow: '0 25px 50px rgba(0,0,0,0.6)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ fontSize: '1.4rem' }}>🔗</span>
                  <h2 style={{ margin: 0, fontSize: '1.4rem', fontWeight: '600', color: 'var(--text-primary)' }}>Share Conversation</h2>
                </div>
                <button onClick={() => setShowShareModal(false)} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', fontSize: '1.4rem', cursor: 'pointer' }}>✕</button>
              </div>

              {shareToastMsg && (
                <div style={{ backgroundColor: 'rgba(34, 197, 94, 0.15)', border: '1px solid rgba(34, 197, 94, 0.4)', color: '#4ade80', padding: '10px 14px', borderRadius: '8px', marginBottom: '16px', fontSize: '0.88rem', fontWeight: '500', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span>✓</span> {shareToastMsg}
                </div>
              )}

              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '16px', lineHeight: '1.5' }}>
                Anyone with this link can view this public PrismAI chat thread:
              </p>

              <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
                <input 
                  type="text" 
                  readOnly 
                  value={`${window.location.origin}/prismai/?share=${currentChatId || 'share-live'}`} 
                  style={{ flex: 1, padding: '10px 12px', backgroundColor: 'var(--input-bg)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-primary)', fontSize: '0.85rem' }} 
                />
                <button 
                  onClick={async () => {
                    const shareUrl = `${window.location.origin}/prismai/?share=${currentChatId || 'share-live'}`;
                    await navigator.clipboard.writeText(shareUrl);
                    setShareToastMsg("Copied shareable link to clipboard! 🔗");
                    setTimeout(() => setShareToastMsg(''), 3000);
                  }}
                  style={{ padding: '10px 16px', backgroundColor: '#a855f7', color: '#fff', border: 'none', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', fontSize: '0.85rem' }}
                >
                  Copy Link
                </button>
              </div>

              <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '16px', marginTop: '16px' }}>
                <span style={{ display: 'block', color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '12px', fontWeight: '600' }}>SHARE TO SOCIAL MEDIA</span>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <a 
                    href={`https://twitter.com/intent/tweet?text=${encodeURIComponent('Check out this AI conversation on PrismAI!')}&url=${encodeURIComponent(`${window.location.origin}/prismai/?share=${currentChatId || 'share-live'}`)}`} 
                    target="_blank" 
                    rel="noreferrer" 
                    style={{ flex: 1, textDecoration: 'none', padding: '8px', backgroundColor: 'rgba(255,255,255,0.06)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-primary)', textAlign: 'center', fontSize: '0.82rem', fontWeight: '500' }}
                  >
                    𝕏 Twitter
                  </a>
                  <a 
                    href={`https://api.whatsapp.com/send?text=${encodeURIComponent(`Check out this PrismAI chat: ${window.location.origin}/prismai/?share=${currentChatId || 'share-live'}`)}`} 
                    target="_blank" 
                    rel="noreferrer" 
                    style={{ flex: 1, textDecoration: 'none', padding: '8px', backgroundColor: 'rgba(34, 197, 94, 0.1)', border: '1px solid rgba(34, 197, 94, 0.3)', borderRadius: '8px', color: '#4ade80', textAlign: 'center', fontSize: '0.82rem', fontWeight: '500' }}
                  >
                    💬 WhatsApp
                  </a>
                  <a 
                    href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(`${window.location.origin}/prismai/?share=${currentChatId || 'share-live'}`)}`} 
                    target="_blank" 
                    rel="noreferrer" 
                    style={{ flex: 1, textDecoration: 'none', padding: '8px', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '8px', color: '#60a5fa', textAlign: 'center', fontSize: '0.82rem', fontWeight: '500' }}
                  >
                    💼 LinkedIn
                  </a>
                </div>
              </div>

              <div style={{ marginTop: '20px', textAlign: 'right' }}>
                <button onClick={() => setShowShareModal(false)} style={{ padding: '8px 18px', backgroundColor: 'var(--input-bg)', color: 'var(--text-primary)', border: '1px solid var(--border-color)', borderRadius: '8px', cursor: 'pointer' }}>
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Tutor Chat Widget Removed per user request */}
    </div>
  )
}

export default App
