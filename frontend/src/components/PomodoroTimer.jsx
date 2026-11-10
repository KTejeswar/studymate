import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Clock } from 'lucide-react';

export default function PomodoroTimer() {
  const [mode, setMode] = useState(25); // 25 or 5 minutes
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    let interval = null;
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setIsRunning(false);
      // Optional audio beep / alert
    }
    return () => clearInterval(interval);
  }, [isRunning, timeLeft]);

  const toggleTimer = () => {
    setIsRunning(!isRunning);
  };

  const resetTimer = (newMinutes = mode) => {
    setIsRunning(false);
    setMode(newMinutes);
    setTimeLeft(newMinutes * 60);
  };

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  const totalSeconds = mode * 60;
  const progressPercent = ((totalSeconds - timeLeft) / totalSeconds) * 100;

  // SVG ring parameters
  const size = 54;
  const strokeWidth = 3.5;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (progressPercent / 100) * circumference;

  return (
    <div className="bg-[#121222] border border-white/10 rounded-2xl p-3.5 space-y-2.5">
      <div className="flex items-center justify-between text-xs text-slate-300">
        <span className="flex items-center gap-1.5 font-semibold">
          <Clock className="w-3.5 h-3.5 text-[#22E4FF]" />
          Study Timer
        </span>
        <div className="flex items-center gap-1 text-[10px]">
          <button
            type="button"
            onClick={() => resetTimer(25)}
            className={`px-1.5 py-0.5 rounded ${mode === 25 ? 'bg-[#5B21B6] text-white font-bold' : 'text-slate-400 hover:text-white'}`}
          >
            25m
          </button>
          <button
            type="button"
            onClick={() => resetTimer(5)}
            className={`px-1.5 py-0.5 rounded ${mode === 5 ? 'bg-[#22E4FF] text-slate-950 font-bold' : 'text-slate-400 hover:text-white'}`}
          >
            5m
          </button>
        </div>
      </div>

      <div className="flex items-center justify-between gap-3">
        {/* SVG Circular Ring with Time Display */}
        <div className="relative w-[54px] h-[54px] shrink-0 flex items-center justify-center">
          <svg className="w-full h-full -rotate-90">
            <circle
              cx={size / 2}
              cy={size / 2}
              r={radius}
              stroke="rgba(255,255,255,0.08)"
              strokeWidth={strokeWidth}
              fill="transparent"
            />
            <circle
              cx={size / 2}
              cy={size / 2}
              r={radius}
              stroke="url(#timerGradient)"
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-300 ease-linear"
            />
            <defs>
              <linearGradient id="timerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#B794FF" />
                <stop offset="100%" stopColor="#22E4FF" />
              </linearGradient>
            </defs>
          </svg>
          <span className="absolute font-mono text-xs font-bold text-white tracking-tight">
            {formattedTime}
          </span>
        </div>

        {/* Play/Pause & Reset Controls */}
        <div className="flex items-center gap-1.5">
          <button
            type="button"
            onClick={toggleTimer}
            className={`p-2 rounded-xl text-xs font-semibold flex items-center justify-center transition shadow-md ${
              isRunning 
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30' 
                : 'bg-gradient-to-r from-[#B794FF] to-[#22E4FF] text-slate-950 hover:opacity-90'
            }`}
            title={isRunning ? 'Pause' : 'Start Focus Session'}
          >
            {isRunning ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5 fill-current" />}
          </button>

          <button
            type="button"
            onClick={() => resetTimer(mode)}
            className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white transition border border-white/10"
            title="Reset"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
