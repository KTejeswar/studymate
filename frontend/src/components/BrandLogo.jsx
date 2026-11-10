import React from 'react';

export default function BrandLogo({ size = 'md', showText = true, showTagline = true }) {
  const isLg = size === 'lg';
  const isSm = size === 'sm';

  return (
    <div className="flex items-center gap-3 select-none">
      {/* Glass card container matching image */}
      <div className={`relative flex items-center justify-center rounded-2xl border border-white/20 bg-gradient-to-b from-white/10 to-white/5 backdrop-blur-md shadow-lg shadow-violet-950/40 shrink-0 ${
        isLg ? 'w-16 h-16' : isSm ? 'w-9 h-9' : 'w-11 h-11'
      }`}>
        <svg
          viewBox="0 0 100 100"
          className={isLg ? 'w-11 h-11' : isSm ? 'w-6 h-6' : 'w-7 h-7'}
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Main 4-point Sparkle Star (Lavender #B794FF) */}
          <path
            d="M50 16 C50 28 58 36 70 36 C58 36 50 44 50 56 C50 44 42 36 30 36 C42 36 50 28 50 16 Z"
            fill="#B794FF"
          />
          {/* Small Accent Sparkle (Cyan #22E4FF) */}
          <path
            d="M72 18 C72 22 74 24 78 24 C74 24 72 26 72 30 C72 26 70 24 66 24 C70 24 72 22 72 18 Z"
            fill="#22E4FF"
          />
          {/* Open Book Outline (Cyan #22E4FF) */}
          <path
            d="M20 54 C30 50 45 52 50 57 C55 52 70 50 80 54 L80 78 C70 74 55 76 50 81 C45 76 30 74 20 78 Z"
            stroke="#22E4FF"
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d="M50 57 L50 81"
            stroke="#22E4FF"
            strokeWidth="3.5"
            strokeLinecap="round"
          />
        </svg>
      </div>

      {showText && (
        <div>
          <div className="flex items-baseline">
            <span className={`font-extrabold tracking-tight text-white ${isLg ? 'text-3xl' : 'text-xl'}`}>
              Study
            </span>
            <span className={`font-extrabold tracking-tight bg-gradient-to-r from-[#B794FF] to-[#22E4FF] bg-clip-text text-transparent ${isLg ? 'text-3xl' : 'text-xl'}`}>
              Mate
            </span>
          </div>
          {showTagline && (
            <p className="text-[11px] text-slate-400 font-medium">
              Your notes, answered. With citations.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
