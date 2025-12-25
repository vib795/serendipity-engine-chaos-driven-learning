'use client';

import { motion } from 'framer-motion';
import { Sparkles, RefreshCw } from 'lucide-react';

interface GenerateButtonProps {
  onClick: () => void;
  isLoading: boolean;
  hasConnection: boolean;
}

export function GenerateButton({ onClick, isLoading, hasConnection }: GenerateButtonProps) {
  return (
    <motion.button
      onClick={onClick}
      disabled={isLoading}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className="relative group disabled:cursor-not-allowed"
    >
      {/* Glow effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full blur-xl opacity-50 group-hover:opacity-75 transition-opacity" />

      {/* Button */}
      <div className="relative px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full text-white font-semibold text-lg shadow-2xl flex items-center gap-3">
        {isLoading ? (
          <>
            <RefreshCw className="w-5 h-5 animate-spin" />
            <span>Finding Connection...</span>
          </>
        ) : hasConnection ? (
          <>
            <RefreshCw className="w-5 h-5" />
            <span>Discover Another</span>
          </>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            <span>Generate Connection</span>
          </>
        )}
      </div>

      {/* Particle effects on hover */}
      <motion.div
        initial={false}
        animate={isLoading ? { rotate: 360 } : { rotate: 0 }}
        transition={{ duration: 2, repeat: isLoading ? Infinity : 0, ease: "linear" }}
        className="absolute inset-0 pointer-events-none"
      >
        {[...Array(6)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-yellow-400 rounded-full"
            style={{
              top: '50%',
              left: '50%',
            }}
            animate={{
              x: [0, Math.cos(i * 60 * Math.PI / 180) * 60],
              y: [0, Math.sin(i * 60 * Math.PI / 180) * 60],
              opacity: [0, 1, 0],
              scale: [0, 1, 0],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              delay: i * 0.2,
            }}
          />
        ))}
      </motion.div>
    </motion.button>
  );
}
