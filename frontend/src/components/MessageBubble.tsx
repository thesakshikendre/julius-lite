import React from "react";

interface Props {
  role: "user" | "assistant";
  children: React.ReactNode;
}

const MessageBubble: React.FC<Props> = ({ role, children }) => (
  <div className={`message ${role}`}>
    <div className="bubble">{children}</div>
  </div>
);

export default MessageBubble;
