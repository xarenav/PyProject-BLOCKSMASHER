import { ArrowLeft, Trophy, Medal, Award, User, Calendar, Target } from 'lucide-react';
import { motion } from 'motion/react';
import { useState } from 'react';
import { IconButton } from './IconButton';
import { GlassCard } from './GlassCard';

interface LeaderboardScreenProps {
  onBack: () => void;
}

interface Score {
  rank: number;
  player: string;
  level: string;
  score: number;
  date: string;
}

const mockScores: Score[] = [
  { rank: 1, player: 'CyberAce', level: 'Level 1', score: 15420, date: '2025-10-05' },
  { rank: 2, player: 'NeonKnight', level: 'Level 1', score: 14850, date: '2025-10-04' },
  { rank: 3, player: 'GlowMaster', level: 'Level 1', score: 13990, date: '2025-10-03' },
  { rank: 4, player: 'BlockBuster', level: 'Level 1', score: 12750, date: '2025-10-02' },
  { rank: 5, player: 'PixelPro', level: 'Level 1', score: 11820, date: '2025-10-01' },
  { rank: 6, player: 'ArcadeHero', level: 'Level 1', score: 10950, date: '2025-09-30' },
  { rank: 7, player: 'RetroGamer', level: 'Level 1', score: 9870, date: '2025-09-29' },
  { rank: 8, player: 'SpeedRunner', level: 'Level 1', score: 8920, date: '2025-09-28' },
];

export function LeaderboardScreen({ onBack }: LeaderboardScreenProps) {
  const [activeTab, setActiveTab] = useState<'all' | 'level1' | 'level2' | 'level3'>('all');
  const [playerName, setPlayerName] = useState('');

  const tabs = [
    { id: 'all' as const, label: 'All Levels', color: 'cyan' },
    { id: 'level1' as const, label: 'Level 1', color: 'purple' },
    { id: 'level2' as const, label: 'Level 2', color: 'orange' },
    { id: 'level3' as const, label: 'Level 3', color: 'cyan' },
  ];

  const topThree = mockScores.slice(0, 3);
  const restOfScores = mockScores.slice(3);

  const totalGames = mockScores.length;
  const highestScore = Math.max(...mockScores.map(s => s.score));
  const averageScore = Math.floor(mockScores.reduce((acc, s) => acc + s.score, 0) / mockScores.length);

  return (
    <div className="relative w-full min-h-screen p-8">
      {/* Background */}
      <div 
        className="absolute inset-0 -z-10"
        style={{
          background: `
            radial-gradient(circle at 20% 20%, rgba(64, 224, 208, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 140, 0, 0.1) 0%, transparent 50%),
            var(--bg-dark)
          `,
        }}
      />

      <div className="max-w-5xl mx-auto">
        <GlassCard className="p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <IconButton size="md" onClick={onBack}>
                <ArrowLeft size={20} />
              </IconButton>
              <div>
                <h2 className="text-3xl font-bold" style={{ color: 'var(--color-orange)' }}>
                  Leaderboard
                </h2>
                <p className="text-sm text-[var(--color-foreground)]/60 mt-1">
                  Top scores from all players
                </p>
              </div>
            </div>
            <button className="glass px-4 py-2 rounded-lg text-sm text-[var(--color-foreground)]/60 hover:text-[var(--color-foreground)] transition-colors">
              Clear All
            </button>
          </div>

          {/* Player Name Input */}
          <div className="glass rounded-lg p-4 mb-8">
            <div className="flex items-center gap-3">
              <User size={20} className="text-[var(--color-cyan)]" />
              <div className="flex-1">
                <label className="text-sm font-semibold block mb-2">Your Name</label>
                <input
                  type="text"
                  value={playerName}
                  onChange={(e) => setPlayerName(e.target.value)}
                  placeholder="Enter your name"
                  className="w-full bg-transparent border border-[var(--color-cyan)]/30 rounded-lg px-3 py-2 text-[var(--color-foreground)] focus:border-[var(--color-cyan)] focus:outline-none transition-colors"
                />
              </div>
            </div>
          </div>

          {/* Top 3 Podium */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
              <Trophy size={20} className="text-yellow-400" />
              <h3 className="font-bold">Top Champions</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {topThree.map((score, index) => {
                const icons = [
                  { Icon: Trophy, color: 'text-yellow-400', borderColor: 'rgba(255, 215, 0, 0.5)' },
                  { Icon: Medal, color: 'text-gray-300', borderColor: 'rgba(192, 192, 192, 0.5)' },
                  { Icon: Award, color: 'text-orange-400', borderColor: 'rgba(205, 127, 50, 0.5)' },
                ];
                const { Icon, color, borderColor } = icons[index];

                return (
                  <GlassCard 
                    key={score.rank} 
                    className="text-center"
                    style={{ borderColor }}
                    glow={index === 0}
                  >
                    <Icon size={20} className={`${color} mx-auto mb-2`} />
                    <p className="font-bold mb-1">{score.player}</p>
                    <p className="text-2xl font-black text-[var(--color-cyan)] mb-2">
                      {score.score.toLocaleString()}
                    </p>
                    <span className="inline-block px-2 py-1 rounded text-xs bg-[var(--color-purple)]/20 text-[var(--color-purple)]">
                      {score.level}
                    </span>
                  </GlassCard>
                );
              })}
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center mb-8">
            <div className="glass rounded-lg p-1 grid grid-cols-4 w-full max-w-2xl">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  className={`flex items-center justify-center h-10 rounded-md transition-all duration-300 text-sm font-semibold ${
                    activeTab === tab.id 
                      ? 'bg-[var(--color-cyan)]/10 text-[var(--color-cyan)] box-glow-cyan' 
                      : 'text-[var(--color-foreground)]/60'
                  }`}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Score Table */}
          <div className="mb-8">
            {/* Header */}
            <div className="grid grid-cols-12 gap-4 px-4 py-2 text-sm font-semibold text-[var(--color-foreground)]/60 mb-2">
              <div className="col-span-1">Rank</div>
              <div className="col-span-3">Player</div>
              <div className="col-span-3">Level</div>
              <div className="col-span-2">Score</div>
              <div className="col-span-3">Date</div>
            </div>

            {/* Rows */}
            <div className="space-y-2">
              {restOfScores.map((score, index) => (
                <motion.div
                  key={score.rank}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="glass rounded-lg px-4 py-3 hover:border-[var(--color-cyan)]/50 transition-all duration-300"
                >
                  <div className="grid grid-cols-12 gap-4 items-center text-sm">
                    <div className="col-span-1 text-[var(--color-foreground)]/60">
                      #{score.rank}
                    </div>
                    <div className="col-span-3 font-semibold">
                      {score.player}
                    </div>
                    <div className="col-span-3">
                      <span className="inline-block px-2 py-1 rounded text-xs border border-[var(--color-cyan)]/30 text-[var(--color-cyan)]">
                        {score.level}
                      </span>
                    </div>
                    <div className="col-span-2 font-bold text-[var(--color-cyan)]">
                      {score.score.toLocaleString()}
                    </div>
                    <div className="col-span-3 flex items-center gap-2 text-[var(--color-foreground)]/60">
                      <Calendar size={12} />
                      <span className="text-xs">{score.date}</span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <GlassCard className="text-center">
              <p className="text-2xl font-bold text-[var(--color-cyan)] mb-1">
                {totalGames}
              </p>
              <p className="text-sm text-[var(--color-foreground)]/60">Total Games</p>
            </GlassCard>
            <GlassCard className="text-center">
              <p className="text-2xl font-bold text-[var(--color-orange)] mb-1">
                {highestScore.toLocaleString()}
              </p>
              <p className="text-sm text-[var(--color-foreground)]/60">Highest Score</p>
            </GlassCard>
            <GlassCard className="text-center">
              <p className="text-2xl font-bold text-[var(--color-purple)] mb-1">
                {averageScore.toLocaleString()}
              </p>
              <p className="text-sm text-[var(--color-foreground)]/60">Average Score</p>
            </GlassCard>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
