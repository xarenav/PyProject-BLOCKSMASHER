import { motion } from 'motion/react';

interface FloatingBlockProps {
  size: number;
  top: string;
  right: string;
  delay?: number;
}

export function FloatingBlock({ size, top, right, delay = 0 }: FloatingBlockProps) {
  return (
    <motion.div
      className="absolute rounded-lg border border-[var(--color-cyan)]/30"
      style={{
        width: size,
        height: size,
        top,
        right,
        background: 'linear-gradient(135deg, rgba(147, 112, 219, 0.2), rgba(64, 224, 208, 0.2))',
        transform: 'rotate(45deg)',
      }}
      animate={{
        y: [0, -20, 0],
        rotate: [45, 50, 45],
      }}
      transition={{
        duration: 6 + delay,
        repeat: Infinity,
        ease: 'easeInOut',
        delay: delay * 0.5,
      }}
    />
  );
}
