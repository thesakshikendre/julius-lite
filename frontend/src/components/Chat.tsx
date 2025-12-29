import React, { useState, useRef, useEffect } from "react";
import { askQuestion, ChatMessage, AnalysisResult } from "../api";
import MessageBubble from "./MessageBubble";

interface Props {
  sessionId: string;
  model: string;
}

const Chat: React.FC<Props> = ({ sessionId, model }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastResult, setLastResult] = useState<AnalysisResult | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg: ChatMessage = { role: "user", content: input };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const result = await askQuestion({
        question: userMsg.content,
        messages: newMessages,
        model,
        session_id: sessionId,
      });

      const assistantMsg: ChatMessage = { role: "assistant", content: result.answer };
      setMessages([...newMessages, assistantMsg]);
      setLastResult(result);
    } catch (e: any) {
      const errorMsg: ChatMessage = {
        role: "assistant",
        content: `Error: ${e.response?.data?.detail || e.message}`,
      };
      setMessages([...newMessages, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} role={msg.role}>
            {msg.content}
          </MessageBubble>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="bubble">Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {lastResult && (
        <div className="result-panel">
          <div className="sql-code">
            <strong>SQL:</strong>
            <pre>{lastResult.code}</pre>
          </div>
          {lastResult.table && lastResult.columns && (
            <div className="result-table">
              <table>
                <thead>
                  <tr>
                    {lastResult.columns.map((c) => (
                      <th key={c}>{c}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {lastResult.table.map((row, idx) => (
                    <tr key={idx}>
                      {lastResult.columns!.map((c) => (
                        <td key={c}>{String(row[c] ?? "")}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <div className="input-container">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask about your data"
          className="chat-input"
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
