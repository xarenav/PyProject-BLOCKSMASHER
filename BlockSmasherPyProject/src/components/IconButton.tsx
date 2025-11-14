import { ButtonHTMLAttributes, ReactNode } from 'react';
import { motion } from 'motion/react';

interface IconButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  size?: 'sm' | 'md' | 'lg';
}

export function IconButton({ children, size = 'md', className = '', ...props }: IconButtonProps) {
  const sizeStyles = {
    sm: 'w-10 h-10',
    md: 'w-12 h-12',
    lg: 'w-14 h-14'
  };
  
  return (
    <motion.button
      className={`${sizeStyles[size]} glass rounded-lg flex items-center justify-center text-[var(--color-cyan)] hover:bg-[var(--color-cyan)]/20 hover:box-glow-cyan transition-all duration-300 ${className}`}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      {...props}
    >
      {children}
    </motion.button>
  );
}
