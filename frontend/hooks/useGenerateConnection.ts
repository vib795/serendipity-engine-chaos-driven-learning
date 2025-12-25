import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { connectionService } from '@/services/connectionService';
import { Connection, Topic } from '@/types/connection';

interface UseGenerateConnectionReturn {
  connection: Connection | null;
  topicA: Topic | null;
  topicB: Topic | null;
  isGenerating: boolean;
  error: string | null;
  generate: () => void;
  generateCustom: (topicA: string, topicB: string) => void;
}

export function useGenerateConnection(): UseGenerateConnectionReturn {
  const [connection, setConnection] = useState<Connection | null>(null);
  const [topicA, setTopicA] = useState<Topic | null>(null);
  const [topicB, setTopicB] = useState<Topic | null>(null);
  const [error, setError] = useState<string | null>(null);

  const randomMutation = useMutation({
    mutationFn: connectionService.generateConnection,
    onMutate: () => {
      setError(null);
    },
    onSuccess: (data) => {
      setTopicA(data.topic_a);
      setTopicB(data.topic_b);
      setConnection(data.connection);
    },
    onError: (err: Error) => {
      setError(err.message || 'Failed to generate connection. Please try again.');
    },
  });

  const customMutation = useMutation({
    mutationFn: ({ topicA, topicB }: { topicA: string; topicB: string }) =>
      connectionService.generateCustomConnection(topicA, topicB),
    onMutate: () => {
      setError(null);
    },
    onSuccess: (data) => {
      setTopicA(data.topic_a);
      setTopicB(data.topic_b);
      setConnection(data.connection);
    },
    onError: (err: Error) => {
      setError(err.message || 'Failed to generate connection. Please try again.');
    },
  });

  const generate = useCallback(() => {
    // Clear previous connection to show loading state
    setConnection(null);
    setTopicA(null);
    setTopicB(null);

    // Then start generating
    randomMutation.mutate();
  }, [randomMutation]);

  const generateCustom = useCallback((topicA: string, topicB: string) => {
    if (!topicA.trim() || !topicB.trim()) {
      setError('Please enter both topics');
      return;
    }

    // Clear previous connection to show loading state
    setConnection(null);
    setTopicA(null);
    setTopicB(null);

    // Then start generating
    customMutation.mutate({ topicA, topicB });
  }, [customMutation]);

  return {
    connection,
    topicA,
    topicB,
    isGenerating: randomMutation.isPending || customMutation.isPending,
    error,
    generate,
    generateCustom,
  };
}
