'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, ChevronDown, Shuffle, Edit3 } from 'lucide-react';
import { ConnectionDisplay } from '@/components/connection/ConnectionDisplay';
import { GenerateButton } from '@/components/connection/GenerateButton';
import { TopicBubble } from '@/components/connection/TopicBubble';
import { ThinkingAnimation } from '@/components/animations/ThinkingAnimation';
import { useGenerateConnection } from '@/hooks/useGenerateConnection';

export default function HomePage() {
  const {
    connection,
    topicA,
    topicB,
    isGenerating,
    generate,
    generateCustom,
    error
  } = useGenerateConnection();

  const [showHow, setShowHow] = useState(false);
  const [mode, setMode] = useState<'random' | 'custom'>('random');
  const [customTopicA, setCustomTopicA] = useState('');
  const [customTopicB, setCustomTopicB] = useState('');

  const handleGenerate = () => {
    if (mode === 'random') {
      generate();
    } else {
      generateCustom(customTopicA, customTopicB);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Hero Section */}
        <header className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 rounded-full mb-6"
          >
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span className="text-sm text-white/80">Automate Serendipity</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-5xl md:text-7xl font-bold text-white mb-4"
          >
            Serendipity Engine
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-white/60 max-w-2xl mx-auto"
          >
            Discover unexpected connections between completely unrelated topics.
            Innovation begins where ideas collide.
          </motion.p>
        </header>

        {/* Main Generator Area */}
        <div className="max-w-4xl mx-auto">
          {/* Mode Toggle */}
          <div className="flex justify-center mb-8">
            <div className="inline-flex bg-white/10 rounded-full p-1">
              <button
                onClick={() => setMode('random')}
                className={`px-6 py-2 rounded-full font-medium transition-all flex items-center gap-2 ${
                  mode === 'random'
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                    : 'text-white/60 hover:text-white/80'
                }`}
              >
                <Shuffle className="w-4 h-4" />
                Random Topics
              </button>
              <button
                onClick={() => setMode('custom')}
                className={`px-6 py-2 rounded-full font-medium transition-all flex items-center gap-2 ${
                  mode === 'custom'
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                    : 'text-white/60 hover:text-white/80'
                }`}
              >
                <Edit3 className="w-4 h-4" />
                Custom Topics
              </button>
            </div>
          </div>

          {/* Custom Topic Inputs */}
          <AnimatePresence mode="wait">
            {mode === 'custom' && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-8"
              >
                <div className="grid md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                  <div>
                    <label className="block text-white/60 text-sm mb-2">Topic A</label>
                    <input
                      type="text"
                      value={customTopicA}
                      onChange={(e) => setCustomTopicA(e.target.value)}
                      placeholder="e.g., Quantum Physics"
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-white/60 text-sm mb-2">Topic B</label>
                    <input
                      type="text"
                      value={customTopicB}
                      onChange={(e) => setCustomTopicB(e.target.value)}
                      placeholder="e.g., Jazz Music"
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Generate Button */}
          <div className="flex justify-center mb-12">
            <GenerateButton
              onClick={handleGenerate}
              isLoading={isGenerating}
              hasConnection={!!connection}
            />
          </div>

          {/* Topics Display */}
          <AnimatePresence mode="wait">
            {(topicA || topicB) && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="flex items-center justify-center gap-8 mb-8 flex-wrap"
              >
                {topicA && <TopicBubble topic={topicA} side="left" />}

                {isGenerating && (
                  <ThinkingAnimation />
                )}

                {topicB && <TopicBubble topic={topicB} side="right" />}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Connection Display */}
          <AnimatePresence mode="wait">
            {connection && !isGenerating && (
              <ConnectionDisplay
                connection={connection}
                topicA={topicA!}
                topicB={topicB!}
              />
            )}
          </AnimatePresence>

          {/* Error Display */}
          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center text-red-400 bg-red-400/10 rounded-xl p-4 max-w-2xl mx-auto"
            >
              {error}
            </motion.div>
          )}
        </div>

        {/* How It Works */}
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-24 max-w-3xl mx-auto"
        >
          <button
            onClick={() => setShowHow(!showHow)}
            className="w-full flex items-center justify-center gap-2 text-white/60 hover:text-white/80 transition-colors"
          >
            <span>How does this work?</span>
            <ChevronDown className={`w-4 h-4 transition-transform ${showHow ? 'rotate-180' : ''}`} />
          </button>

          <AnimatePresence>
            {showHow && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="overflow-hidden"
              >
                <div className="grid md:grid-cols-3 gap-6 mt-8">
                  <HowItWorksStep
                    number={1}
                    title="Choose Your Mode"
                    description="Pick random topics from our diverse sources, or enter your own custom topics to explore."
                  />
                  <HowItWorksStep
                    number={2}
                    title="AI Analysis"
                    description="Our AI examines both topics, looking for shared themes, historical parallels, and conceptual bridges."
                  />
                  <HowItWorksStep
                    number={3}
                    title="Revelation"
                    description="You discover a genuine intellectual connection you never would have found on your own."
                  />
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.section>
      </div>
    </main>
  );
}

function HowItWorksStep({ number, title, description }: {
  number: number;
  title: string;
  description: string;
}) {
  return (
    <div className="text-center p-6 bg-white/5 rounded-2xl">
      <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
        <span className="text-white font-bold">{number}</span>
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-white/60 text-sm">{description}</p>
    </div>
  );
}
