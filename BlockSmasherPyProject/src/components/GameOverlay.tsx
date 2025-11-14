import { Trophy, RotateCcw, ArrowLeft, XCircle } from 'lucide-react';
import { motion } from 'motion/react';

interface GameOverlayProps {
  type: 'pause' | 'victory' | 'defeat';
  score: number;
  onRestart: () => void;
  onMenu: () => void;
  onResume?: () => void;
  mapNumber?: number;
  showStars?: boolean;
}

export function GameOverlay({ type, score, onRestart, onMenu, onResume, mapNumber, showStars = false }: GameOverlayProps) {
  if (type === 'pause') {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
        className="absolute inset-0 flex items-center justify-center"
        style={{
          background: 'rgba(10, 14, 26, 0.8)',
          backdropFilter: 'blur(4px)',
        }}
      >
        <div className="text-center">
          <h2 
            className="text-5xl font-bold mb-4 glow-cyan"
            style={{ color: 'var(--color-cyan)' }}
          >
            PAUSED
          </h2>
          <p className="text-[var(--color-foreground)]/60">
            Press the play button to continue
          </p>
        </div>
      </motion.div>
    );
  }

  const isVictory = type === 'victory';
  const glowColor = isVictory ? 'cyan' : 'orange';
  const borderColor = isVictory ? 'var(--color-cyan)' : 'var(--color-orange)';
  const glowClass = isVictory ? 'box-glow-cyan' : 'box-glow-orange';

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="absolute inset-0 flex items-center justify-center"
      style={{
        background: 'rgba(10, 14, 26, 0.9)',
        backdropFilter: 'blur(8px)',
      }}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        className={`glass rounded-xl p-8 min-w-[400px] text-center ${glowClass}`}
        style={{
          borderWidth: '2px',
          borderColor: `${borderColor}`,
          background: 'rgba(20, 25, 40, 0.6)',
        }}
      >
        {/* Icon */}
        <motion.div
          animate={isVictory ? { 
            scale: [1, 1.05, 1],
          } : {
            rotate: [-3, 0, 3, 0],
          }}
          transition={isVictory ? {
            duration: 0.6,
            repeat: Infinity,
            ease: 'easeInOut',
          } : {
            duration: 0.4,
            ease: 'easeInOut',
          }}
          className="mb-4"
        >
          {isVictory ? (
            <Trophy 
              size={64} 
              className="mx-auto"
              style={{
                color: borderColor,
                filter: `drop-shadow(0 0 20px ${borderColor})`,
              }}
            />
          ) : (
            <XCircle 
              size={64} 
              className="mx-auto"
              style={{
                color: borderColor,
                filter: `drop-shadow(0 0 20px ${borderColor})`,
              }}
            />
          )}
        </motion.div>

        {/* Title */}
        <motion.h2
          animate={{
            textShadow: [
              `0 0 20px ${borderColor}99, 0 0 40px ${borderColor}4D`,
              `0 0 25px ${borderColor}CC, 0 0 50px ${borderColor}66`,
              `0 0 20px ${borderColor}99, 0 0 40px ${borderColor}4D`,
            ],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="text-5xl font-bold mb-2 tracking-wider"
          style={{ 
            color: borderColor,
            letterSpacing: '0.05em',
          }}
        >
          {isVictory ? 'VICTORY!' : 'GAME OVER'}
        </motion.h2>

        {/* Map Number if provided */}
        {mapNumber && isVictory && (
          <p className="text-xl mb-2 text-[var(--color-foreground)]/80">
            You perfectly finished map #{mapNumber}
          </p>
        )}

        {/* Stars if showStars is true */}
        {showStars && isVictory && (
          <div className="flex gap-2 justify-center mb-4">
            {[...Array(3)].map((_, i) => (
              <motion.span
                key={i}
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ 
                  delay: i * 0.15,
                  type: 'spring',
                  stiffness: 200,
                  damping: 10
                }}
                className="text-4xl"
                style={{
                  color: '#FFD700',
                  filter: 'drop-shadow(0 0 10px #FFD700)',
                }}
              >
                ★
              </motion.span>
            ))}
          </div>
        )}

        {/* Score */}
        <p className="text-2xl font-semibold mb-6 text-[var(--color-foreground)]">
          Score: {score}
        </p>

        {/* Buttons */}
        <div className="flex gap-3 justify-center">
          <button
            onClick={onRestart}
            className="flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all duration-300"
            style={{
              background: 'var(--color-cyan)',
              color: 'white',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = '0 0 20px rgba(147, 112, 219, 0.5)';
              e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            <RotateCcw size={16} />
            {isVictory ? 'Play Again' : 'Try Again'}
          </button>
          <button
            onClick={onMenu}
            className="flex items-center gap-2 px-6 py-3 rounded-lg font-semibold glass border-2 transition-all duration-300"
            style={{
              borderColor: 'rgba(255, 255, 255, 0.3)',
              color: 'var(--color-foreground)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.5)';
              e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)';
              e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.3)';
              e.currentTarget.style.background = 'rgba(20, 25, 40, 0.4)';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            <ArrowLeft size={16} />
            Back to Maps
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}
