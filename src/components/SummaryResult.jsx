// src/components/SummaryResult.jsx
import jsPDF from "jspdf";

export default function SummaryResult({ result }) {
  if (!result) return null;

  const downloadFile = (text, filename) => {
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadPDF = (text, filename) => {
    const pdf = new jsPDF();
    const lines = pdf.splitTextToSize(text, 180);
    pdf.text(lines, 10, 10);
    pdf.save(filename);
  };

  const saveToHistory = () => {
    const email = localStorage.getItem("current_user");
    console.log("🪪 current_user in saveToHistory:", email);
    if (!email) return alert("로그인이 필요합니다.");
    const title = prompt("요약 제목을 입력하세요:");
    if (!title) return;

    const key = `summaries__${email}`;
    const prev = JSON.parse(localStorage.getItem(key) || "[]");
    const createdAt = new Date().toISOString();
    const newEntry = { title, text: result, createdAt, isImportant: false };
    const updated = [newEntry, ...prev.slice(0, 9)];
    localStorage.setItem(key, JSON.stringify(updated));
    alert("이전 요약에 저장되었습니다.");
  };

  return (
    <div className="card bg-base-100 shadow-xl mb-6">
      <div className="card-body">
        <h2 className="card-title">요약 결과</h2>
        <p>{result}</p>
        <div className="card-actions justify-end flex-wrap gap-2">
          <button className="btn btn-outline btn-sm" onClick={() => navigator.clipboard.writeText(result)}>복사</button>
          <button className="btn btn-outline btn-sm" onClick={() => downloadFile(result, "summary.txt")}>.txt 다운로드</button>
          <button className="btn btn-outline btn-sm" onClick={() => downloadPDF(result, "summary.pdf")}>.pdf 다운로드</button>
          <button className="btn btn-outline btn-sm" onClick={saveToHistory}>이전 요약에 저장</button>
        </div>
      </div>
    </div>
  );
}