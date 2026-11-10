import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Sparkles, 
  User, 
  BookOpen, 
  Layers, 
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { api } from '../lib/api';

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am StudyMate. Ask me anything from your class notes, and I will cite the exact file and page!',
      citations: [],
      steps: [],
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [expandedCitation, setExpandedCitation] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userText }]);
    setLoading(true);

    try {
      const res = await api.sendChatMessage(userText);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.answer,
          citations: res.citations || [],
          steps: res.steps || [],
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error while searching your notes. Please make sure the backend is running.',
          citations: [],
          steps: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-2rem)] max-w-4xl mx-auto p-4 animate-fade-in">
      {/* Banner */}
      <div className="py-2.5 px-4 mb-3 rounded-xl bg-[#5B21B6]/20 border border-[#B794FF]/30 flex items-center justify-between text-xs text-[#22E4FF]">
        <span className="flex items-center gap-2 font-medium">
          <BookOpen className="w-3.5 h-3.5 text-[#B794FF]" />
          Grounded Q&A: StudyMate answers strictly from uploaded notes with file & page citations.
        </span>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#5B21B6] to-[#22E4FF] flex items-center justify-center text-white shrink-0 mt-1 shadow-md">
                <Sparkles className="w-4 h-4" />
              </div>
            )}

            <div className={`max-w-[85%] space-y-2 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div
                className={`p-4 rounded-2xl text-sm leading-relaxed shadow-lg ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-[#5B21B6] to-[#7C3AED] text-white rounded-br-none'
                    : 'bg-[#0B0B14] border border-white/10 text-slate-200 rounded-bl-none'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>
              </div>

              {/* Citations Chips */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="space-y-1.5 pt-1">
                  <div className="flex items-center gap-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    <BookOpen className="w-3 h-3 text-[#22E4FF]" />
                    Citations ({msg.citations.length})
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {msg.citations.map((cite, cIdx) => {
                      const isExpanded = expandedCitation === `${i}-${cIdx}`;
                      return (
                        <div key={cIdx} className="flex flex-col">
                          <button
                            onClick={() => setExpandedCitation(isExpanded ? null : `${i}-${cIdx}`)}
                            className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs bg-[#22E4FF]/10 text-[#22E4FF] border border-[#22E4FF]/30 hover:bg-[#22E4FF]/20 transition"
                          >
                            <span className="font-semibold">{cite.filename}</span>
                            <span className="text-slate-400">• P.{cite.page}</span>
                            {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                          </button>

                          {isExpanded && (
                            <div className="mt-1.5 p-3 rounded-lg bg-[#121222] border border-white/10 text-xs text-slate-300 max-w-sm">
                              <p className="font-semibold text-[#B794FF] mb-1">
                                Source Excerpt:
                              </p>
                              <p className="italic">"{cite.snippet}"</p>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Steps Log */}
              {msg.steps && msg.steps.length > 0 && (
                <details className="text-[11px] text-slate-500 pt-1 cursor-pointer">
                  <summary className="hover:text-slate-300 inline-flex items-center gap-1">
                    <Layers className="w-3 h-3" />
                    Agent trace: {msg.steps.length} steps executed
                  </summary>
                  <ul className="mt-1 pl-3 border-l-2 border-violet-800 space-y-0.5 text-[10px] font-mono text-slate-400">
                    {msg.steps.map((st, sIdx) => (
                      <li key={sIdx}>{st}</li>
                    ))}
                  </ul>
                </details>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center text-slate-300 shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 justify-start items-center text-slate-400 text-xs">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#5B21B6] to-[#22E4FF] flex items-center justify-center text-white shrink-0 shadow-sm animate-pulse">
              <Sparkles className="w-4 h-4" />
            </div>
            <div className="p-3 bg-[#0B0B14] border border-white/10 rounded-2xl rounded-bl-none flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-[#22E4FF] animate-bounce" />
              <div className="w-2 h-2 rounded-full bg-[#22E4FF] animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 rounded-full bg-[#22E4FF] animate-bounce [animation-delay:0.4s]" />
              <span className="text-xs text-slate-400 ml-1">Evaluating question & retrieving chunks...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Question Starter Chips */}
      <div className="pt-2 pb-1">
        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-1 text-xs">
          <span className="text-[11px] font-semibold text-slate-400 shrink-0 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-[#22E4FF]" />
            Suggestions:
          </span>
          {[
            "Summarize the core concepts of my notes",
            "What are the most likely exam questions?",
            "Explain key definitions and formulas",
            "Give a quick 3-bullet revision sheet"
          ].map((promptText, idx) => (
            <button
              key={idx}
              type="button"
              disabled={loading}
              onClick={() => {
                setInput(promptText);
              }}
              className="shrink-0 px-3 py-1 rounded-full bg-white/5 hover:bg-[#22E4FF]/10 border border-white/10 hover:border-[#22E4FF]/40 text-slate-300 hover:text-[#22E4FF] transition text-[11px] font-medium"
            >
              {promptText}
            </button>
          ))}
        </div>
      </div>

      {/* Input Form */}
      <form onSubmit={handleSend} className="pt-3">
        <div className="flex items-center gap-2 p-1.5 rounded-2xl bg-[#0B0B14] border border-white/10 shadow-xl focus-within:ring-2 focus-within:ring-[#22E4FF]">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your uploaded notes..."
            className="flex-1 px-4 py-2 text-sm bg-transparent text-white focus:outline-none"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="p-2.5 rounded-xl bg-gradient-to-r from-[#B794FF] to-[#22E4FF] text-slate-950 font-bold disabled:opacity-40 hover:opacity-90 transition"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
}
