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
}

export function useGenerateConnection(): UseGenerateConnectionReturn {
  const [connection, setConnection] = useState<Connection | null>(null);
  const [topicA, setTopicA] = useState<Topic | null>(null);
  const [topicB, setTopicB] = useState<Topic | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
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

  const generate = useCallback(() => {
    // Clear previous connection to show loading state
    setConnection(null);
    setTopicA(null);
    setTopicB(null);

    // Then start generating
    mutation.mutate();
  }, [mutation]);

  return {
    connection,
    topicA,
    topicB,
    isGenerating: mutation.isPending,
    error,
    generate,
  };
}
