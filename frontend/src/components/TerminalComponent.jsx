import React, { useEffect, useRef, useState } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

export const TerminalComponent = ({ terminalRef, onTerminalInit }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const term = new Terminal({
      convertEol: true,
      cursorBlink: true,
      theme: {
        background: '#0d0d0d',
        foreground: '#e0e0e0',
        cursor: '#4ade80',
        selectionBackground: 'rgba(74, 222, 128, 0.3)',
      },
      fontFamily: '"JetBrains Mono", monospace',
      fontSize: 12,
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(containerRef.current);
    fitAddon.fit();

    if (onTerminalInit) {
      onTerminalInit(term);
    }

    // Handle window resize
    const resizeObserver = new ResizeObserver(() => {
      fitAddon.fit();
    });
    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
      term.dispose();
    };
  }, []);

  return (
    <div 
      ref={containerRef} 
      style={{ width: '100%', height: '100%', backgroundColor: '#0d0d0d', padding: '12px' }}
    />
  );
};
