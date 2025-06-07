// src/pages/History.jsx
import { useEffect, useState } from "react";

export default function History() {
  const [summaries, setSummaries] = useState([]);
  const [expandedIndex, setExpandedIndex] = useState(null); // ⬅ 펼침 상태 관리

  useEffect(() => {
    const email = localStorage.getItem("current_user");
    const key = `summaries__${email}`;
    const saved = JSON.parse(localStorage.getItem(key) || "[]");
    setSummaries(saved);
  }, []);

  const updateStorage = (updated) => {
    const email = localStorage.getItem("current_user");
    const key = `summaries__${email}`;
    setSummaries(updated);
    localStorage.setItem(key, JSON.stringify(updated));
  };

  const handleDelete = (index) => {
    const updated = [...summaries];
    updated.splice(index, 1);
    updateStorage(updated);
    if (expandedIndex === index) setExpandedIndex(null);
  };

  const toggleImportant = (index) => {
    const updated = summaries.map((item, i) =>
      i === index ? { ...item, isImportant: !item.isImportant } : item
    );
    updated.sort((a, b) => b.isImportant - a.isImportant);
    updateStorage(updated);
  };

  const clearAll = () => {
    if (window.confirm("정말 모든 요약을 삭제하시겠습니까?")) {
      updateStorage([]);
      setExpandedIndex(null);
    }
  };

  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString(undefined, {
      year: "numeric",
      month: "numeric",
      day: "numeric",
      hour: "numeric",
      minute: "numeric"
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">이전 요약 기록</h2>
        <button className="btn btn-sm btn-outline btn-error" onClick={clearAll}>전체 삭제</button>
      </div>
      {summaries.length === 0 ? (
        <p className="text-sm text-gray-400">저장된 요약이 없습니다.</p>
      ) : (
        <ul className="space-y-2">
          {summaries.map((item, idx) => (
            <li key={idx} className="bg-base-100 p-4 rounded shadow">
              {/* 제목 클릭 시 펼침/접힘 토글 */}
              <div
                className="flex justify-between items-start cursor-pointer"
                onClick={() => setExpandedIndex(expandedIndex === idx ? null : idx)}
              >
                <div className="flex-1 mr-4">
                  <p className="font-semibold">📄 {item.title || "(제목 없음)"}</p>
                  <p className="text-xs text-gray-400">{formatDate(item.createdAt)}</p>
                </div>
                <div className="flex flex-col gap-1 items-center">
                  <button className="text-2xl btn btn-ghost p-0 h-auto min-h-0" onClick={(e) => { e.stopPropagation(); toggleImportant(idx); }}>
                    {item.isImportant ? (
                      <span className="text-yellow-400">★</span>
                    ) : (
                      <span className="text-gray-400">☆</span>
                    )}
                  </button>
                  <button className="btn btn-xs btn-error" onClick={(e) => { e.stopPropagation(); handleDelete(idx); }}>
                    삭제
                  </button>
                </div>
              </div>

              {/* 펼쳐진 요약 내용 */}
              {expandedIndex === idx && (
                <div className="mt-3 px-2 text-sm whitespace-pre-wrap border-t border-gray-700 pt-2 text-gray-300">
                  {item.text || item.summary}
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
