import { Play, Map, Trophy, HelpCircle, User, Settings, Users } from 'lucide-react';
import { motion } from 'motion/react';
import { GlassButton } from './GlassButton';
import { IconButton } from './IconButton';
import { FloatingBlock } from './FloatingBlock';

interface MainMenuProps {
  onNavigate: (screen: string) => void;
}

export function MainMenu({ onNavigate }: MainMenuProps) {
  return (
    <div className="relative w-full min-h-screen overflow-hidden">
      {/* Animated Background */}
      <div 
        className="absolute inset-0"
        style={{
          background: `
            radial-gradient(circle at 20% 20%, rgba(64, 224, 208, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 140, 0, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(147, 112, 219, 0.1) 0%, transparent 50%),
            linear-gradient(135deg, #0a0e1a 0%, #1a1530 25%, #0f1a2a 50%, #1a0f20 75%, #0a0e1a 100%)
          `,
        }}
      >
        {/* Diagonal Line Pattern */}
        <div 
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `
              repeating-linear-gradient(45deg, transparent, transparent 60px, rgba(147, 112, 219, 1) 60px, rgba(147, 112, 219, 1) 61px),
              repeating-linear-gradient(-45deg, transparent, transparent 60px, rgba(64, 224, 208, 1) 60px, rgba(64, 224, 208, 1) 61px)
            `
          }}
        />
      </div>

      {/* Vertical Light Beam */}
      <div 
        className="absolute top-0 bottom-0 right-[40%] w-px opacity-50"
        style={{
          background: 'linear-gradient(to bottom, transparent, rgba(64, 224, 208, 0.5) 50%, transparent)',
          filter: 'blur(40px)',
          transform: 'skewX(-10deg)',
        }}
      />

      {/* Floating Blocks */}
      <FloatingBlock size={80} top="15%" right="20%" delay={0} />
      <FloatingBlock size={60} top="45%" right="15%" delay={1} />
      <FloatingBlock size={100} top="70%" right="25%" delay={2} />
      <FloatingBlock size={70} top="25%" right="35%" delay={1.5} />

      {/* Top-right Icon Navigation */}
      <motion.div 
        className="absolute top-6 right-6 flex gap-4 z-20"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, staggerChildren: 0.1 }}
      >
        <IconButton><HelpCircle size={24} /></IconButton>
        <IconButton><User size={24} /></IconButton>
        <IconButton onClick={() => onNavigate('settings')}><Settings size={24} /></IconButton>
        <IconButton><Users size={24} /></IconButton>
      </motion.div>

      {/* Main Content */}
      <div className="relative z-10 flex items-center min-h-screen px-16">
        <motion.div 
          className="w-full max-w-md"
          initial={{ opacity: 0, x: -100 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
        >
          {/* Title */}
          <div className="mb-16">
            <h1 className="text-7xl font-bold tracking-wide">
              <span className="glow-cyan" style={{ color: 'var(--color-cyan)' }}>BLOCK</span>
            </h1>
            <h1 className="text-7xl font-bold tracking-wide">
              <span className="glow-orange" style={{ color: 'var(--color-orange)' }}>SMASHER</span>
            </h1>
            <div 
              className="mt-4 h-[3px] w-48 rounded-full box-glow-cyan"
              style={{
                background: 'linear-gradient(90deg, var(--color-cyan), var(--color-purple), var(--color-orange))'
              }}
            />
          </div>

          {/* Menu Items */}
          <motion.div 
            className="flex flex-col gap-3"
            initial={{ opacity: 0, x: -100 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2, staggerChildren: 0.1 }}
          >
            <GlassButton 
              icon={<Play size={20} />} 
              onClick={() => onNavigate('maps')}
            >
              PLAY
            </GlassButton>
            <GlassButton 
              icon={<Map size={20} />}
              onClick={() => onNavigate('maps')}
            >
              MAPS
            </GlassButton>
            <GlassButton 
              icon={<Trophy size={20} />}
              onClick={() => onNavigate('leaderboard')}
            >
              LEADERBOARD
            </GlassButton>
          </motion.div>

          {/* Info Card */}
          <motion.div 
            className="mt-12 glass rounded-lg p-4"
            initial={{ opacity: 0, x: -100 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <p className="text-sm text-[var(--color-foreground)]/60">PREMIUM EDITION</p>
            <p className="text-xs text-[var(--color-foreground)]/40 mt-1">Version 1.0.0</p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
