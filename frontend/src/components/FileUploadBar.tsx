import React from "react";

interface Props {
  onFileSelected: (file: File) => void;
  model: string;
  setModel: (m: string) => void;
}

const FileUploadBar: React.FC<Props> = ({ onFileSelected, model, setModel }) => (
  <div className="upload-bar">
    <input
      type="file"
      accept=".csv"
      onChange={(e) => e.target.files && onFileSelected(e.target.files[0])}
      className="file-input"
    />
    <select value={model} onChange={(e) => setModel(e.target.value)} className="model-select">
      <option value="gpt-4o-mini">GPT-4o-mini</option>
      <option value="gemini-1.5-flash">Gemini</option>
    </select>
  </div>
);

export default FileUploadBar;
