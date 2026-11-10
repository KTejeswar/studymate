import React, { useEffect, useState } from 'react';
import { 
  FileText, 
  GraduationCap, 
  Target, 
  HelpCircle, 
  ArrowRight,
  TrendingDown,
  RefreshCw,
  Sparkles,
  Flame,
  Award,
  CheckCircle2,
  Lock
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  Cell 
} from 'recharts';
import { api } from '../lib/api';
import BrandLogo from './BrandLogo';

export default function Dashboard({ onStartWeakQuiz, onNavigateNotes }) {
  const [summary, setSummary] = useState(null);
  const [weakTopics, setWeakTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [sumRes, weakRes] = await Promise.all([
        api.getStatsSummary().catch(() => ({ total_notes: 0, total_quizzes_taken: 0, average_score: 0, total_questions_answered: 0 })),
        api.getWeakTopics().catch(() => ({ weak_topics: [] })),
      ]);
      setSummary(sumRes);
      setWeakTopics(weakRes.weak_topics || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const statsCards = [
    {
      title: 'Uploaded Notes',
      value: summary?.total_notes ?? 0,
      icon: FileText,
      gradient: 'from-[#5B21B6] to-[#7C3AED]',
    },
    {
      title: 'Quizzes Taken',
      value: summary?.total_quizzes_taken ?? 0,
      icon: GraduationCap,
      gradient: 'from-[#22E4FF] to-[#0284C7]',
    },
    {
      title: 'Average Score',
      value: `${summary?.average_score ?? 0}%`,
      icon: Target,
      gradient: 'from-[#B794FF] to-[#8B5CF6]',
    },
    {
      title: 'Questions Answered',
      value: summary?.total_questions_answered ?? 0,
      icon: HelpCircle,
      gradient: 'from-[#10B981] to-[#059669]',
    },
  ];

  const chartData = weakTopics.map((item) => ({
    topic: item.topic.length > 18 ? item.topic.slice(0, 15) + '...' : item.topic,
    fullTopic: item.topic,
    errorRate: item.error_rate,
    wrong: item.wrong,
    total: item.total_attempts,
  }));

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8 animate-fade-in">
      {/* ── HERO BANNER: CLEAN & MINIMAL ──────────────────────── */}
      <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-r from-[#0B0B18] via-[#0E0B22] to-[#08131D] p-8 shadow-2xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div className="flex items-center gap-6">
            <BrandLogo size="lg" showText={false} />
            <div>
              <div className="flex items-baseline">
                <span className="text-3xl md:text-5xl font-extrabold tracking-tight text-white">
                  Study
                </span>
                <span className="text-3xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-[#B794FF] to-[#22E4FF] bg-clip-text text-transparent">
                  Mate
                </span>
              </div>
              <p className="text-sm md:text-base text-slate-300 font-medium mt-1">
                Your notes, answered. With citations.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onNavigateNotes}
              className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-xs font-semibold text-white transition border border-white/10"
            >
              Upload Notes
            </button>
            <button
              onClick={() => onStartWeakQuiz(null)}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-[#B794FF] to-[#22E4FF] text-slate-950 text-xs font-bold transition hover:opacity-95 shadow-md"
            >
              Start Quiz
            </button>
          </div>
        </div>
      </div>

      {/* ── STATS CARDS ────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statsCards.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <div
              key={idx}
              className="bg-[#0B0B14] rounded-2xl p-5 border border-white/10 hover:border-[#B794FF]/40 transition group shadow-lg"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  {stat.title}
                </span>
                <div className={`p-2.5 rounded-xl bg-gradient-to-tr ${stat.gradient} text-white shadow-md group-hover:scale-105 transition`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div className="text-2xl font-bold mt-3 text-white">
                {loading ? <div className="h-8 w-16 bg-white/10 rounded animate-pulse" /> : stat.value}
              </div>
            </div>
          );
        })}
      </div>

      {/* ── GAMIFIED ACHIEVEMENTS & STUDY STREAK ──────────────── */}
      <div className="bg-[#0B0B14] border border-white/10 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/10">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-gradient-to-tr from-amber-500 to-orange-500 text-white shadow-md">
              <Flame className="w-5 h-5 fill-current animate-pulse" />
            </div>
            <div>
              <h3 className="font-bold text-base text-white flex items-center gap-2">
                Study Streak: <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-orange-400">3 Days Active</span>
              </h3>
              <p className="text-xs text-slate-400">Keep practicing daily to maintain your momentum!</p>
            </div>
          </div>
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[#22E4FF]">
            Level 2 Scholar
          </span>
        </div>

        {/* 4 Milestones / Badges */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-1">
          {[
            {
              title: "Note Pioneer",
              desc: "Uploaded notes to vault",
              achieved: (summary?.total_notes ?? 0) > 0,
              icon: FileText,
              color: "text-[#22E4FF] border-[#22E4FF]/40 bg-[#22E4FF]/10",
            },
            {
              title: "Quiz Explorer",
              desc: "Completed first quiz",
              achieved: (summary?.total_quizzes_taken ?? 0) > 0,
              icon: GraduationCap,
              color: "text-[#B794FF] border-[#B794FF]/40 bg-[#B794FF]/10",
            },
            {
              title: "Accuracy Ace",
              desc: "Scored 75%+ average",
              achieved: (summary?.average_score ?? 0) >= 75,
              icon: Target,
              color: "text-emerald-400 border-emerald-500/40 bg-emerald-500/10",
            },
            {
              title: "Targeted Master",
              desc: "Practiced weak topics",
              achieved: (summary?.total_quizzes_taken ?? 0) >= 2,
              icon: Award,
              color: "text-amber-400 border-amber-500/40 bg-amber-500/10",
            },
          ].map((badge, bIdx) => {
            const BadgeIcon = badge.icon;
            return (
              <div
                key={bIdx}
                className={`p-3.5 rounded-xl border transition-all ${
                  badge.achieved
                    ? `${badge.color} shadow-md`
                    : "border-white/5 bg-white/[0.02] text-slate-500 opacity-60"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <BadgeIcon className="w-4 h-4" />
                  {badge.achieved ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <Lock className="w-3.5 h-3.5 text-slate-600" />
                  )}
                </div>
                <h4 className="text-xs font-bold text-white mb-0.5">{badge.title}</h4>
                <p className="text-[10px] text-slate-400 leading-tight">{badge.desc}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── WEAK TOPICS CHART & ACTION ─────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-[#0B0B14] rounded-2xl p-6 border border-white/10 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-semibold text-base flex items-center gap-2 text-white">
                <Target className="w-4 h-4 text-[#22E4FF]" />
                Weakest Topics Analysis
              </h3>
              <p className="text-xs text-slate-400">
                Topics with highest error rate from quizzes taken
              </p>
            </div>
            <button
              onClick={loadData}
              className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-white px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 transition"
            >
              <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>

          {chartData.length > 0 ? (
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                  <defs>
                    {/* Glowing lavender-to-cyan gradient */}
                    <linearGradient id="weakBarGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#22E4FF" stopOpacity={0.9} />
                      <stop offset="50%" stopColor="#B794FF" stopOpacity={0.85} />
                      <stop offset="100%" stopColor="#5B21B6" stopOpacity={0.7} />
                    </linearGradient>
                  </defs>
                  <XAxis 
                    dataKey="topic" 
                    tick={{ fontSize: 11, fill: '#94A3B8' }} 
                    interval={0}
                    angle={-15}
                    textAnchor="end"
                  />
                  <YAxis unit="%" tick={{ fontSize: 11, fill: '#94A3B8' }} domain={[0, 100]} />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="bg-[#0B0B18] border border-[#B794FF]/30 text-white text-xs p-3 rounded-xl shadow-2xl space-y-1">
                            <p className="font-bold text-[#22E4FF]">{data.fullTopic}</p>
                            <p className="text-[#B794FF] font-medium">Error Rate: {data.errorRate}%</p>
                            <p className="text-slate-400">Missed: {data.wrong} of {data.total} attempts</p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Bar dataKey="errorRate" fill="url(#weakBarGradient)" radius={[8, 8, 2, 2]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-64 flex flex-col items-center justify-center text-center p-6 border border-dashed border-white/10 rounded-xl">
              <GraduationCap className="w-10 h-10 text-slate-600 mb-2" />
              <p className="text-sm font-medium text-slate-300">No quiz attempts recorded yet</p>
              <p className="text-xs text-slate-500 mt-1 max-w-sm">
                Take a practice quiz on your class notes to start populating this weak-topics chart.
              </p>
            </div>
          )}
        </div>

        {/* Action card */}
        <div className="rounded-2xl p-6 text-white shadow-xl flex flex-col justify-between border border-[#B794FF]/30 bg-gradient-to-br from-[#5B21B6]/60 via-[#1A0B2E]/70 to-[#0A1224]/80">
          <div className="space-y-3">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#B794FF]/20 text-[#B794FF] text-xs font-semibold border border-[#B794FF]/30">
              <Sparkles className="w-3.5 h-3.5" />
              Adaptive Study
            </span>
            <h3 className="text-xl font-bold leading-snug">
              Master your weakest concepts
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Click any topic below to generate a focused practice quiz targeting that specific concept:
            </p>

            {/* List of ALL weak topics to practice */}
            {weakTopics.length > 0 ? (
              <div className="pt-2 flex flex-wrap gap-2 max-h-44 overflow-y-auto pr-1">
                {weakTopics.map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => onStartWeakQuiz(item.topic)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/10 hover:bg-[#22E4FF]/20 hover:border-[#22E4FF]/40 border border-white/10 text-xs font-medium text-slate-200 hover:text-white transition group"
                  >
                    <span>{item.topic}</span>
                    <span className="text-[10px] text-[#B794FF] font-mono group-hover:text-[#22E4FF]">
                      ({item.error_rate}%)
                    </span>
                  </button>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-400 italic pt-2">
                No weak topics detected yet. Take a quiz to reveal concepts needing review!
              </p>
            )}
          </div>

          <div className="pt-6">
            {weakTopics.length > 0 ? (
              <button
                onClick={() => onStartWeakQuiz(weakTopics[0].topic)}
                className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-gradient-to-r from-[#B794FF] to-[#22E4FF] text-slate-950 font-bold text-sm hover:opacity-95 shadow-lg transition"
              >
                <span>Practice Weakest: {weakTopics[0].topic.slice(0, 16)}...</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={onNavigateNotes}
                className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-gradient-to-r from-[#B794FF] to-[#22E4FF] text-slate-950 font-bold text-sm hover:opacity-95 shadow-lg transition"
              >
                <span>Upload Class Notes</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
