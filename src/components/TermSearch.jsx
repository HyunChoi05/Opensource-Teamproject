// src/components/TermSearch.jsx
import { useState } from "react";

export default function TermSearch() {
  const [term, setTerm] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!term.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`http://localhost:5000/api/wiki?term=${encodeURIComponent(term)}`);
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({ type: "error", message: "서버 연결 오류" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6 space-y-4">
      <div className="flex gap-2">
        <input
          type="text"
          className="input input-bordered w-full"
          placeholder="용어를 입력하세요"
          value={term}
          onChange={(e) => setTerm(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button className="btn btn-primary" onClick={handleSearch}>검색</button>
      </div>

      <div className="card bg-base-100 shadow">
        <div className="card-body">
          <h2 className="card-title">검색 결과</h2>
          {loading && <p>🔄 검색 중...</p>}
          {!loading && result && (
            <>
              {result.type === "definition" && <p>{result.content}</p>}
              {result.type === "disambiguation" && (
                <ul className="list-disc list-inside">
                  {result.options.slice(0, 10).map((option, idx) => (
                    <li key={idx}>{option}</li>
                  ))}
                </ul>
              )}
              {result.type === "error" && <p className="text-red-500">❌ {result.message}</p>}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
