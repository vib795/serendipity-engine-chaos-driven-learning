export interface Topic {
  id: string;
  source: 'wikipedia' | 'pokemon' | 'trivia' | 'fact' | 'number' | 'quote';
  source_id?: string;
  title: string;
  summary: string;
  full_content?: string;
  category?: string;
  tags: string[];
  image_url?: string;
  source_url?: string;
  created_at?: string;
}

export interface Connection {
  id: string;
  topic_a_id: string;
  topic_b_id: string;
  title: string;
  summary: string;
  detailed_explanation: string;
  connection_type: 'thematic' | 'historical' | 'scientific' | 'metaphorical' | 'structural' | 'cultural';
  bridge_concepts: string[];
  creativity_score: number;
  plausibility_score: number;
  view_count: number;
  favorite_count: number;
  share_count?: number;
  model_used?: string;
  generation_time_ms?: number;
  created_at: string;
}

export interface GenerateConnectionResponse {
  topic_a: Topic;
  topic_b: Topic;
  connection: Connection;
}

export interface ConnectionResponse {
  connection: Connection;
  topic_a: Topic;
  topic_b: Topic;
}
