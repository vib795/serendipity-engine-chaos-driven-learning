'use client';

import { motion } from 'framer-motion';
import { Heart, Share2, ExternalLink, Check } from 'lucide-react';
import { useState } from 'react';
import { Connection, Topic } from '@/types/connection';

interface ConnectionDisplayProps {
  connection: Connection;
  topicA: Topic;
  topicB: Topic;
}

export function ConnectionDisplay({ connection, topicA, topicB }: ConnectionDisplayProps) {
  const [isFavorited, setIsFavorited] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    const url = `${window.location.origin}/connection/${connection.id}`;
    await navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const connectionTypeColors: Record<string, string> = {
    thematic: 'from-purple-500 to-pink-500',
    historical: 'from-amber-500 to-orange-500',
    scientific: 'from-cyan-500 to-blue-500',
    metaphorical: 'from-green-500 to-emerald-500',
    structural: 'from-indigo-500 to-violet-500',
    cultural: 'from-rose-500 to-red-500',
  };

  const gradientClass = connectionTypeColors[connection.connection_type] || 'from-purple-500 to-blue-500';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
      className="relative"
    >
      {/* Main Card */}
      <div className="bg-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20">
        {/* Header */}
        <div className="flex items-start justify-between mb-6 flex-wrap gap-4">
          <div>
            <span className={`inline-block px-3 py-1 text-xs font-medium rounded-full bg-gradient-to-r ${gradientClass} text-white mb-3`}>
              {connection.connection_type.charAt(0).toUpperCase() + connection.connection_type.slice(1)} Connection
            </span>
            <h2 className="text-2xl md:text-3xl font-bold text-white">
              {connection.title}
            </h2>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => setIsFavorited(!isFavorited)}
              className={`p-2 rounded-full transition-colors ${
                isFavorited
                  ? 'bg-red-500 text-white'
                  : 'bg-white/10 text-white/60 hover:bg-white/20'
              }`}
            >
              <Heart className={`w-5 h-5 ${isFavorited ? 'fill-current' : ''}`} />
            </button>
            <button
              onClick={handleShare}
              className="p-2 rounded-full bg-white/10 text-white/60 hover:bg-white/20 transition-colors"
            >
              {copied ? <Check className="w-5 h-5 text-green-400" /> : <Share2 className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Summary */}
        <p className="text-xl text-white/80 mb-6 leading-relaxed">
          {connection.summary}
        </p>

        {/* Bridge Concepts */}
        <div className="flex flex-wrap gap-2 mb-6">
          {connection.bridge_concepts.map((concept, index) => (
            <span
              key={index}
              className="px-3 py-1 bg-white/10 rounded-full text-sm text-white/70"
            >
              {concept}
            </span>
          ))}
        </div>

        {/* Detailed Explanation */}
        <div className="bg-black/20 rounded-2xl p-6 mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">The Connection Explained</h3>
          <div className="text-white/70 space-y-4 leading-relaxed">
            {connection.detailed_explanation.split('\n\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        </div>

        {/* Source Topics */}
        <div className="grid md:grid-cols-2 gap-4">
          <TopicSourceCard topic={topicA} label="Topic A" />
          <TopicSourceCard topic={topicB} label="Topic B" />
        </div>
      </div>
    </motion.div>
  );
}

function TopicSourceCard({ topic, label }: { topic: Topic; label: string }) {
  return (
    <div className="bg-white/5 rounded-xl p-4">
      <span className="text-xs text-white/40 uppercase tracking-wider">{label}</span>
      <h4 className="text-white font-medium mt-1">{topic.title}</h4>
      <p className="text-white/50 text-sm mt-2 line-clamp-2">{topic.summary}</p>
      {topic.source_url && (
        <a
          href={topic.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-xs text-purple-400 hover:text-purple-300 mt-3"
        >
          Learn more <ExternalLink className="w-3 h-3" />
        </a>
      )}
    </div>
  );
}
