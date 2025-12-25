'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

export function ThinkingAnimation() {
  const thoughts = [
    "Analyzing patterns...",
    "Finding bridges...",
    "Connecting dots...",
    "Discovering links...",
  ];

  const [currentThought, setCurrentThought] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentThought((prev) => (prev + 1) % thoughts.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center gap-4">
      {/* Neural network visualization */}
      <div className="relative w-24 h-24">
        {/* Center node */}
        <motion.div
          className="absolute top-1/2 left-1/2 w-4 h-4 bg-purple-500 rounded-full -translate-x-1/2 -translate-y-1/2"
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 1, repeat: Infinity }}
        />

        {/* Orbiting nodes */}
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-pink-400 rounded-full"
            style={{
              top: '50%',
              left: '50%',
            }}
            animate={{
              x: Math.cos((i * 60) * Math.PI / 180) * 40,
              y: Math.sin((i * 60) * Math.PI / 180) * 40,
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        ))}

        {/* Connection lines */}
        <svg className="absolute inset-0 w-full h-full">
          {[0, 1, 2, 3, 4, 5].map((i) => (
            <motion.line
              key={i}
              x1="50%"
              y1="50%"
              x2={`${50 + Math.cos(i * 60 * Math.PI / 180) * 40}%`}
              y2={`${50 + Math.sin(i * 60 * Math.PI / 180) * 40}%`}
              stroke="rgba(168, 85, 247, 0.3)"
              strokeWidth="1"
              animate={{ opacity: [0.3, 0.8, 0.3] }}
              transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}
            />
          ))}
        </svg>
      </div>

      {/* Rotating text */}
      <div className="text-white/60 text-sm h-6">
        <AnimatePresence mode="wait">
          <motion.span
            key={currentThought}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            {thoughts[currentThought]}
          </motion.span>
        </AnimatePresence>
      </div>
    </div>
  );
}
