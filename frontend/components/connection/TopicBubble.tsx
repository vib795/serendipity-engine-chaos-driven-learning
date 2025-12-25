'use client';

import { motion } from 'framer-motion';
import { Topic } from '@/types/connection';
import { ExternalLink } from 'lucide-react';

interface TopicBubbleProps {
  topic: Topic;
  side: 'left' | 'right';
}

export function TopicBubble({ topic, side }: TopicBubbleProps) {
  const sourceColors: Record<string, string> = {
    wikipedia: 'from-blue-500 to-cyan-500',
    pokemon: 'from-red-500 to-yellow-500',
    trivia: 'from-green-500 to-emerald-500',
    fact: 'from-purple-500 to-pink-500',
    number: 'from-orange-500 to-red-500',
    quote: 'from-indigo-500 to-purple-500',
  };

  const gradientClass = sourceColors[topic.source] || 'from-purple-500 to-blue-500';

  return (
    <motion.div
      initial={{ opacity: 0, x: side === 'left' ? -50 : 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: side === 'left' ? -50 : 50 }}
      transition={{ duration: 0.5 }}
      className="max-w-xs"
    >
      <div className="relative">
        {/* Glow */}
        <div className={`absolute inset-0 bg-gradient-to-br ${gradientClass} rounded-2xl blur-xl opacity-30`} />

        {/* Card */}
        <div className="relative bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
          <div className={`inline-block px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${gradientClass} text-white mb-3`}>
            {topic.source}
          </div>

          <h3 className="text-lg font-semibold text-white mb-2 line-clamp-2">
            {topic.title}
          </h3>

          <p className="text-sm text-white/70 line-clamp-3 mb-4">
            {topic.summary}
          </p>

          {topic.source_url && (
            <a
              href={topic.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-xs text-purple-400 hover:text-purple-300 transition-colors"
            >
              Learn more <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>
      </div>
    </motion.div>
  );
}
