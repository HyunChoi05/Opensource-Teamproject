// src/pages/Summary.jsx
import { useState } from "react";
import SummaryInput from "../components/SummaryInput";
import SummaryResult from "../components/SummaryResult";

export default function Summary() {
  const [result, setResult] = useState("");

  return (
    <div className="space-y-6">
      <SummaryInput onSummarize={setResult} />
      <SummaryResult result={result} />
    </div>
  );
}
