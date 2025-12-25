import api from './api';
import { GenerateConnectionResponse, ConnectionResponse } from '@/types/connection';

export const connectionService = {
  async generateConnection(): Promise<GenerateConnectionResponse> {
    const response = await api.post<GenerateConnectionResponse>('/connections/generate');
    return response.data;
  },

  async generateCustomConnection(topicA: string, topicB: string): Promise<GenerateConnectionResponse> {
    const response = await api.post<GenerateConnectionResponse>('/connections/generate-custom', {
      topic_a: topicA,
      topic_b: topicB,
    });
    return response.data;
  },

  async getConnection(id: string): Promise<ConnectionResponse> {
    const response = await api.get<ConnectionResponse>(`/connections/${id}`);
    return response.data;
  },

  async listConnections(skip: number = 0, limit: number = 10): Promise<ConnectionResponse[]> {
    const response = await api.get<ConnectionResponse[]>('/connections/', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getPopularConnections(limit: number = 10): Promise<ConnectionResponse[]> {
    const response = await api.get<ConnectionResponse[]>('/connections/popular', {
      params: { limit },
    });
    return response.data;
  },
};
