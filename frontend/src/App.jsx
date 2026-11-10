import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import Notes from './components/Notes';
import Chat from './components/Chat';
import Quiz from './components/Quiz';

export default function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [activeWeakTopic, setActiveWeakTopic] = useState(null);

  const handleStartWeakQuiz = (topic) => {
    setActiveWeakTopic(topic);
    setCurrentTab('quiz');
  };

  return (
    <div className="relative flex h-screen w-screen overflow-hidden bg-[#05050A] text-slate-100">
      {/* Background ambient radial glow matching colors in banner */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden select-none z-0">
        <div className="absolute top-[-100px] left-[-100px] w-[500px] h-[500px] rounded-full bg-[#5B21B6]/15 blur-[140px]" />
        <div className="absolute bottom-[-100px] right-[-100px] w-[500px] h-[500px] rounded-full bg-[#22E4FF]/10 blur-[140px]" />
      </div>

      {/* Fixed Left Sidebar */}
      <div className="relative z-10 h-full">
        <Sidebar 
          currentTab={currentTab} 
          setCurrentTab={setCurrentTab} 
        />
      </div>

      {/* Main Content Area */}
      <main className="relative z-10 flex-1 overflow-y-auto">
        {currentTab === 'dashboard' && (
          <Dashboard 
            onStartWeakQuiz={handleStartWeakQuiz}
            onNavigateNotes={() => setCurrentTab('notes')}
          />
        )}
        {currentTab === 'notes' && <Notes />}
        {currentTab === 'chat' && <Chat />}
        {currentTab === 'quiz' && (
          <Quiz 
            key={activeWeakTopic || 'default'} 
            initialTopic={activeWeakTopic} 
          />
        )}
      </main>
    </div>
  );
}
