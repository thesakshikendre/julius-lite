import React, { useState } from "react";
import FileUploadBar from "./components/FileUploadBar";
import Chat from "./components/Chat";
import { uploadCsv } from "./api";

const App: React.FC = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [model, setModel] = useState("gpt-4o-mini");
  const [fileInfo, setFileInfo] = useState("Upload CSV to start");

  const handleFile = async (file: File) => {
    try {
      setFileInfo("Uploading...");
      const res = await uploadCsv(file);
      setSessionId(res.session_id);
      setFileInfo(`Loaded tables: ${res.tables.join(", ")}`);
    } catch (e: any) {
      setFileInfo(`Error: ${e.response?.data?.detail || e.message}`);
      setSessionId(null);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Julius AI Clone</h1>
        <p>Upload CSV → Chat with SQL → See code & results</p>
      </header>
      <FileUploadBar onFileSelected={handleFile} model={model} setModel={setModel} />
      <div className="file-status">{fileInfo}</div>
      {sessionId && <Chat sessionId={sessionId} model={model} />}
    </div>
  );
};

export default App;
