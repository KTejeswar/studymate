'use client';

import React from 'react';

export default function MeshBackground() {
  return (
    <div
      aria-hidden="true"
      className="fixed inset-0 pointer-events-none overflow-hidden select-none z-0"
      style={{ opacity: 'var(--mesh-opacity)' }}
    >
      {/* Mesh Layer 1: Electric Lavender */}
      <div
        className="absolute -top-[15%] -left-[10%] w-[65vw] h-[65vw] max-w-[850px] max-h-[850px] rounded-full blur-[140px] animate-blob-1"
        style={{
          background: 'radial-gradient(circle, var(--accent-lavender) 0%, transparent 65%)',
          opacity: 0.28,
        }}
      />

      {/* Mesh Layer 2: Cyber Cyan */}
      <div
        className="absolute top-[35%] -right-[15%] w-[60vw] h-[60vw] max-w-[780px] max-h-[780px] rounded-full blur-[150px] animate-blob-2"
        style={{
          background: 'radial-gradient(circle, var(--accent-cyan) 0%, transparent 60%)',
          opacity: 0.22,
        }}
      />

      {/* Mesh Layer 3: Deep Violet */}
      <div
        className="absolute -bottom-[20%] left-[20%] w-[70vw] h-[70vw] max-w-[900px] max-h-[900px] rounded-full blur-[160px] animate-blob-3"
        style={{
          background: 'radial-gradient(circle, var(--accent-violet) 0%, transparent 70%)',
          opacity: 0.35,
        }}
      />

      {/* Subtle Noise Texture Overlay */}
      <div
        className="absolute inset-0 opacity-[0.035]"
        style={{
          backgroundImage:
            'radial-gradient(rgba(255, 255, 255, 0.4) 1px, transparent 1px)',
          backgroundSize: '24px 24px',
        }}
      />
    </div>
  );
}
