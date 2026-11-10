import React, { useEffect, useState } from 'react';
import { 
  LayoutDashboard, 
  FileText, 
  MessageSquare, 
  GraduationCap
} from 'lucide-react';
import BrandLogo from './BrandLogo';
import PomodoroTimer from './PomodoroTimer';
import { api } from '../lib/api';

export default function Sidebar({ currentTab, setCurrentTab }) {
  const [online, setOnline] = useState(false);

  useEffect(() => {
    api.checkHealth()
      .then(() => setOnline(true))
      .catch(() => setOnline(false));
    const interval = setInterval(() => {
      api.checkHealth()
        .then(() => setOnline(true))
        .catch(() => setOnline(false));
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'notes', label: 'Class Notes', icon: FileText },
    { id: 'chat', label: 'Ask StudyMate', icon: MessageSquare },
    { id: 'quiz', label: 'Take Quiz', icon: GraduationCap },
  ];

  return (
    <aside className="w-64 bg-[#0A0A14] border-r border-white/10 flex flex-col justify-between p-5 select-none shrink-0 h-full">
      <div>
        {/* Brand Icon Only in Sidebar */}
        <div className="py-2 mb-8 flex justify-center">
          <BrandLogo size="md" showText={false} />
        </div>

        {/* Nav Items */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150 ${
                  isActive
                    ? 'bg-gradient-to-r from-[#B794FF]/20 to-[#22E4FF]/10 text-[#22E4FF] border border-[#B794FF]/30 shadow-lg shadow-violet-950/20'
                    : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-[#22E4FF]' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer: Pomodoro Timer + Live Backend Status */}
      <div className="pt-4 border-t border-white/10 space-y-3 px-1">
        <PomodoroTimer />

        <div className="flex items-center justify-between text-xs px-1 text-slate-400 pt-1">
          <span className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${online ? 'bg-[#39FF88] animate-pulse' : 'bg-rose-500'}`} />
            {online ? 'Backend Online' : 'Connecting to API...'}
          </span>
        </div>
      </div>
    </aside>
  );
}
