import { ButtonHTMLAttributes, ReactNode } from 'react';
import { motion } from 'motion/react';

interface GlassButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'default' | 'outline' | 'ghost';
  icon?: ReactNode;
  active?: boolean;
  glowColor?: 'cyan' | 'purple' | 'orange';
}

export function GlassButton({ 
  children, 
  variant = 'default', 
  icon, 
  active = false,
  glowColor = 'cyan',
  className = '', 
  ...props 
}: GlassButtonProps) {
  const baseStyles = "flex items-center gap-3 px-6 py-3 rounded-lg transition-all duration-300 tracking-wide";
  
  const variantStyles = {
    default: `glass ${active ? 'bg-[var(--color-cyan)]/10 border-[var(--color-cyan)]' : ''} hover:bg-[var(--color-cyan)]/10 group`,
    outline: "glass hover:bg-[var(--color-cyan)]/10 group",
    ghost: "hover:bg-[var(--color-cyan)]/5 group"
  };

  const glowStyles = {
    cyan: 'hover:box-glow-cyan',
    purple: 'hover:box-glow-purple',
    orange: 'hover:box-glow-orange'
  };
  
  return (
    <motion.button
      className={`${baseStyles} ${variantStyles[variant]} ${glowStyles[glowColor]} ${className}`}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      {...props}
    >
      {icon && (
        <span className={`text-[var(--color-cyan)] group-hover:text-[var(--color-orange)] transition-colors duration-300`}>
          {icon}
        </span>
      )}
      <span className={`${active ? 'text-[var(--color-cyan)]' : 'text-[var(--color-foreground)]/90'} group-hover:text-[var(--color-cyan)] transition-colors duration-300`}>
        {children}
      </span>
    </motion.button>
  );
}
