import { ReactNode } from 'react';
import { motion } from 'motion/react';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  glow?: boolean;
  onClick?: () => void;
}

export function GlassCard({ children, className = '', hover = false, glow = false, onClick }: GlassCardProps) {
  const Component = onClick ? motion.button : motion.div;
  
  return (
    <Component
      className={`glass rounded-xl p-6 ${hover ? 'hover:border-[var(--color-cyan)] hover:box-glow-cyan cursor-pointer' : ''} ${glow ? 'box-glow-cyan border-[var(--color-cyan)]' : ''} transition-all duration-300 ${className}`}
      whileHover={hover ? { scale: 1.05, y: -5 } : undefined}
      whileTap={onClick ? { scale: 0.98 } : undefined}
      onClick={onClick}
    >
      {children}
    </Component>
  );
}
