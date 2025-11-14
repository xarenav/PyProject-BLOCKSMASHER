import { ArrowLeft, Sparkles, Shuffle, Lock, Unlock, Code2, Zap, Pause, RotateCcw } from 'lucide-react';
import { GameOverlay } from './GameOverlay';
import { IconButton } from './IconButton';
import { motion } from 'motion/react';
import { useState } from 'react';
import { GlassCard } from './GlassCard';

interface MapsScreenProps {
  onBack: () => void;
  onSelectMap: (mapId: number) => void;
  unlockedLevels: number[];
}

interface MapData {
  id: number;
  name: string;
  description: string;
  difficulty: string;
  blocks: number;
  locked: boolean;
  completed?: boolean;
  stars?: number;
}

const curatedMaps: MapData[] = [
  {
    id: 1,
    name: 'First Steps',
    description: 'A gentle introduction to block breaking. Learn the basics and get comfortable with the controls.',
    difficulty: 'Easy',
    blocks: 24,
    locked: false,
    completed: true,
    stars: 3
  },
  {
    id: 2,
    name: 'Circular Formation',
    description: 'Eight blocks arranged in a perfect circle. Can you break them all?',
    difficulty: 'Medium',
    blocks: 8,
    locked: true,
    completed: true,
    stars: 3
  },
  {
    id: 3,
    name: 'Pyramid Power',
    description: 'Navigate through a pyramid formation of increasingly difficult blocks.',
    difficulty: 'Medium',
    blocks: 36,
    locked: true,
    completed: true,
    stars: 3
  },
  {
    id: 4,
    name: 'Checkerboard',
    description: 'An alternating pattern that tests your strategic planning.',
    difficulty: 'Hard',
    blocks: 32,
    locked: true,
    completed: true,
    stars: 3
  },
  {
    id: 5,
    name: 'The Fortress',
    description: 'Break through multiple layers of fortified block defenses.',
    difficulty: 'Hard',
    blocks: 64,
    locked: true,
    completed: true,
    stars: 3
  },
  {
    id: 6,
    name: 'Explosive Chaos',
    description: 'Power-ups and explosions create unpredictable chaos.',
    difficulty: 'Extreme',
    blocks: 80,
    locked: true,
    completed: true,
    stars: 3
  },
];

export function MapsScreen({ onBack, onSelectMap, unlockedLevels }: MapsScreenProps) {
  const [activeTab, setActiveTab] = useState<'curated' | 'procedural'>('curated');
  const [developerMode, setDeveloperMode] = useState(false);
  const [instantWinMode, setInstantWinMode] = useState(false);
  const [devLockStates, setDevLockStates] = useState<{ [key: number]: boolean }>({});
  const [instantWinMapId, setInstantWinMapId] = useState<number | null>(null);

  // Update the locked status based on unlocked levels or dev mode overrides
  const updatedMaps = curatedMaps.map(map => {
    const locked = developerMode 
      ? (devLockStates[map.id] !== undefined ? devLockStates[map.id] : !unlockedLevels.includes(map.id))
      : !unlockedLevels.includes(map.id);
    
    return {
      ...map,
      locked
    };
  });

  const toggleMapLock = (mapId: number, currentLockState: boolean) => {
    setDevLockStates(prev => ({
      ...prev,
      [mapId]: !currentLockState
    }));
  };

  return (
    <div className="relative w-full min-h-screen p-8">
      {/* Background similar to main menu but more subtle */}
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

      <div className="max-w-6xl mx-auto">
        <GlassCard className="p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <IconButton size="md" onClick={onBack}>
                <ArrowLeft size={20} />
              </IconButton>
              <h2 className="text-3xl font-bold" style={{ color: 'var(--color-cyan)' }}>
                Select Map
              </h2>
            </div>
            
            {/* Developer Mode Buttons */}
            <div className="flex flex-col gap-2 items-end">
              <button
                onClick={() => setDeveloperMode(!developerMode)}
                className={`glass px-4 py-2 rounded-lg flex items-center gap-2 transition-all duration-300 ${
                  developerMode 
                    ? 'bg-[var(--color-orange)]/20 text-[var(--color-orange)] box-glow-orange' 
                    : 'text-[var(--color-foreground)]/60 hover:bg-[var(--color-cyan)]/10'
                }`}
              >
                <Code2 size={16} />
                <span className="text-sm font-semibold">Developer Mode</span>
              </button>
              
              {developerMode && (
                <motion.button
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`glass px-4 py-2 rounded-lg flex items-center gap-2 transition-all duration-300 ${
                    instantWinMode 
                      ? 'bg-[var(--color-purple)]/20 text-[var(--color-purple)] box-glow-purple' 
                      : 'text-[var(--color-foreground)]/60 hover:bg-[var(--color-purple)]/10'
                  }`}
                  onClick={() => setInstantWinMode(!instantWinMode)}
                >
                  <Zap size={16} />
                  <span className="text-sm font-semibold">
                    {instantWinMode ? 'Instant Win ON' : 'Instant Win OFF'}
                  </span>
                </motion.button>
              )}
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center mb-8">
            <div className="glass rounded-lg p-1 grid grid-cols-2 max-w-md w-full">
              <button
                className={`flex items-center justify-center gap-2 h-10 rounded-md transition-all duration-300 ${
                  activeTab === 'curated' 
                    ? 'bg-[var(--color-cyan)]/10 text-[var(--color-cyan)] box-glow-cyan' 
                    : 'text-[var(--color-foreground)]/60'
                }`}
                onClick={() => setActiveTab('curated')}
              >
                <Sparkles size={16} />
                <span className="font-semibold">Curated Maps</span>
              </button>
              <button
                className={`flex items-center justify-center gap-2 h-10 rounded-md transition-all duration-300 ${
                  activeTab === 'procedural' 
                    ? 'bg-[var(--color-cyan)]/10 text-[var(--color-cyan)] box-glow-cyan' 
                    : 'text-[var(--color-foreground)]/60'
                }`}
                onClick={() => setActiveTab('procedural')}
              >
                <Shuffle size={16} />
                <span className="font-semibold">Procedural</span>
              </button>
            </div>
          </div>

          {/* Maps Grid */}
          {activeTab === 'curated' ? (
            <motion.div 
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ staggerChildren: 0.05 }}
            >
              {updatedMaps.map((map, index) => (
                <motion.div
                  key={map.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  onClick={() => {
                    if (developerMode && instantWinMode) {
                      setInstantWinMapId(map.id);
                    } else if (!map.locked) {
                      onSelectMap(map.id);
                    }
                  }}
                  className={`${!map.locked || (developerMode && instantWinMode) ? 'cursor-pointer' : ''}`}
                >
                  <GlassCard 
                    hover={!map.locked} 
                    className={`relative ${map.locked ? 'opacity-50' : ''}`}
                  >
                    {/* Developer Mode Lock Toggle */}
                    {developerMode && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleMapLock(map.id, map.locked);
                        }}
                        className="absolute top-2 right-2 z-10 glass p-2 rounded-lg hover:bg-[var(--color-cyan)]/20 transition-all duration-300"
                        style={{ opacity: 1 }}
                      >
                        {map.locked ? (
                          <Lock size={16} className="text-[var(--color-foreground)]/60" />
                        ) : (
                          <Unlock size={16} className="text-[var(--color-cyan)]" />
                        )}
                      </button>
                    )}

                    {/* Preview Area */}
                    <div 
                      className="h-24 rounded-lg border border-[var(--color-cyan)]/30 flex items-center justify-center mb-4"
                      style={{
                        background: 'linear-gradient(135deg, rgba(64, 224, 208, 0.2), rgba(255, 140, 0, 0.2))'
                      }}
                    >
                      <span className="text-5xl font-bold text-[var(--color-cyan)]/30">
                        {map.id}
                      </span>
                    </div>

                    {/* Info Section */}
                    <div>
                      <h3 className="font-bold mb-1">{map.name}</h3>
                      
                      {map.completed && map.stars && (
                        <div className="flex gap-1 mb-2">
                          {[...Array(3)].map((_, i) => (
                            <span key={i} className={i < map.stars ? 'text-yellow-400' : 'text-gray-600'}>
                              ★
                            </span>
                          ))}
                        </div>
                      )}

                      <p className="text-sm text-[var(--color-foreground)]/60 mb-3 line-clamp-2">
                        {map.description}
                      </p>

                      {/* Badges */}
                      <div className="flex gap-2">
                        <span className="px-2 py-1 rounded text-xs bg-[var(--color-purple)]/20 text-[var(--color-purple)]">
                          {map.difficulty}
                        </span>
                        <span className="px-2 py-1 rounded text-xs border border-[var(--color-cyan)]/30 text-[var(--color-cyan)]">
                          {map.blocks} blocks
                        </span>
                      </div>
                    </div>

                    {/* Locked Overlay */}
                    {map.locked && (
                      <div className="absolute inset-0 flex items-center justify-center bg-[var(--bg-dark)]/50 backdrop-blur-sm rounded-xl">
                        <Lock size={32} className="text-[var(--color-foreground)]/40" />
                      </div>
                    )}
                  </GlassCard>
                </motion.div>
              ))}
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div className="flex justify-between items-center mb-4">
                <p className="text-sm text-[var(--color-foreground)]/60">
                  Procedurally generated levels - each number always generates the same pattern
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[...Array(12)].map((_, index) => {
                  const levelId = 100 + index + 1;
                  const difficulty = ['Easy', 'Medium', 'Hard', 'Expert'][Math.floor(index / 3) % 4];
                  const estimatedBlocks = 30 + (index * 5) + (index % 3) * 10;
                  
                  return (
                    <motion.div
                      key={levelId}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      onClick={() => {
                        if (developerMode && instantWinMode) {
                          setInstantWinMapId(levelId);
                        } else {
                          onSelectMap(levelId);
                        }
                      }}
                      className="cursor-pointer"
                    >
                      <GlassCard hover>
                        <div 
                          className="h-24 rounded-lg border border-[var(--color-cyan)]/30 flex items-center justify-center mb-4"
                          style={{
                            background: 'linear-gradient(135deg, rgba(147, 112, 219, 0.2), rgba(64, 224, 208, 0.2))'
                          }}
                        >
                          <div className="flex items-center gap-2">
                            <Shuffle size={28} className="text-[var(--color-cyan)]/40" />
                            <span className="text-4xl font-bold text-[var(--color-purple)]/30">
                              {index + 1}
                            </span>
                          </div>
                        </div>

                        <div>
                          <h3 className="font-bold mb-1">Random Level #{index + 1}</h3>
                          <p className="text-sm text-[var(--color-foreground)]/60 mb-3">
                            A unique procedurally generated challenge
                          </p>

                          <div className="flex gap-2">
                            <span className="px-2 py-1 rounded text-xs bg-[var(--color-purple)]/20 text-[var(--color-purple)]">
                              {difficulty}
                            </span>
                            <span className="px-2 py-1 rounded text-xs border border-[var(--color-cyan)]/30 text-[var(--color-cyan)]">
                              ~{estimatedBlocks} blocks
                            </span>
                          </div>
                        </div>
                      </GlassCard>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          )}
        </GlassCard>
      </div>

      {/* Fullscreen Instant Win Overlay */}
      {instantWinMapId !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-8" style={{ background: 'var(--bg-dark)' }}>
          {/* Game Background */}
          <div className="relative">
            <GlassCard className="p-6">
              {/* Header Info */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-4">
                  <div className="glass px-4 py-2 rounded-lg">
                    <span className="text-sm text-[var(--color-cyan)]">Level: {instantWinMapId}</span>
                  </div>
                  <div className="glass px-4 py-2 rounded-lg">
                    <span className="text-sm text-[var(--color-orange)]">Lives: 3</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <IconButton size="sm">
                    <Pause size={16} />
                  </IconButton>
                  <IconButton size="sm">
                    <RotateCcw size={16} />
                  </IconButton>
                </div>
              </div>

              {/* Game Canvas Area */}
              <div 
                className="relative rounded-lg border-2 overflow-hidden"
                style={{
                  width: '800px',
                  height: '600px',
                  borderColor: 'var(--color-cyan)',
                  background: 'linear-gradient(180deg, rgba(10, 14, 26, 0.95) 0%, rgba(20, 25, 40, 0.95) 100%)',
                  boxShadow: '0 0 30px rgba(64, 224, 208, 0.3)',
                }}
              >
                {/* Cleared game state - no blocks, just paddle */}
                <canvas 
                  width={800} 
                  height={600}
                  ref={(canvas) => {
                    if (canvas) {
                      const ctx = canvas.getContext('2d');
                      if (ctx) {
                        // Clear canvas
                        ctx.clearRect(0, 0, 800, 600);
                        
                        // Draw paddle with gradient
                        const paddleX = 340;
                        const paddleY = 560;
                        const paddleWidth = 120;
                        const paddleHeight = 15;
                        
                        const gradient = ctx.createLinearGradient(paddleX, paddleY, paddleX + paddleWidth, paddleY);
                        gradient.addColorStop(0, '#9333ea');
                        gradient.addColorStop(0.5, '#40e0d0');
                        gradient.addColorStop(1, '#ff8c00');
                        
                        ctx.fillStyle = gradient;
                        ctx.shadowColor = '#40e0d0';
                        ctx.shadowBlur = 15;
                        ctx.fillRect(paddleX, paddleY, paddleWidth, paddleHeight);
                        ctx.shadowBlur = 0;
                      }
                    }
                  }}
                />

                {/* Victory Overlay on top */}
                <GameOverlay
                  type="victory"
                  score={1000}
                  onRestart={() => setInstantWinMapId(null)}
                  onMenu={() => setInstantWinMapId(null)}
                  mapNumber={instantWinMapId}
                  showStars={true}
                />
              </div>

              {/* Footer Info */}
              <div className="mt-4 text-center text-sm text-[var(--color-foreground)]/60">
                Move paddle: Mouse or Arrow Keys | Launch ball: Space or Click
              </div>
            </GlassCard>
          </div>
        </div>
      )}
    </div>
  );
}
