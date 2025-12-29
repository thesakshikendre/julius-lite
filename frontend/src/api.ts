import axios from "axios";

const API_BASE = "http://localhost:8000";

export interface UploadResponse {
  session_id: string;
  tables: string[];
}

export interface AnalysisResult {
  answer: string;
  table?: Record<string, unknown>[];
  columns?: string[];
  chart?: any;
  code: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export async function uploadCsv(file: File): Promise<UploadResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await axios.post(`${API_BASE}/upload`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function askQuestion(params: {
  question: string;
  messages: ChatMessage[];
  model: string;
  session_id: string;
}): Promise<AnalysisResult> {
  const res = await axios.post(`${API_BASE}/ask`, params);
  return res.data;
}
