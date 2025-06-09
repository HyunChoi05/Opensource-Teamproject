import { useState } from "react";
import * as pdfjsLib from "pdfjs-dist";
import worker from "pdfjs-dist/build/pdf.worker.js?worker";

pdfjsLib.GlobalWorkerOptions.workerSrc = worker;

export default function SummaryInput({ onSummarize }) {
  const [text, setText] = useState("");
  const [mode, setMode] = useState("");
  const [loading, setLoading] = useState(false);

  const summarizeText = async (inputText) => {
    try {
      setLoading(true);
      const response = await fetch("http://localhost:5001/api/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText, mode }),
      });

      const data = await response.json();
      if (data.error) {
        alert("요약 실패: " + data.error);
        return;
      }

      onSummarize(data.summary); // 자동 저장 제거됨
    } catch (err) {
      console.error("요약 오류:", err);
      alert("요약 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  const handleClick = () => {
    if (!text.trim()) {
      alert("요약할 텍스트를 입력하거나 파일을 업로드해주세요.");
      return;
    }
    summarizeText(text);
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const ext = file.name.split(".").pop().toLowerCase();

    if (["txt", "md", "csv", "json"].includes(ext)) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = ext === "json"
          ? JSON.stringify(JSON.parse(event.target.result), null, 2)
          : event.target.result;
        setText(content);
        summarizeText(content);
      };
      reader.readAsText(file);
    } else if (ext === "pdf") {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("mode", mode);

      try {
        setLoading(true);
        const response = await fetch("http://localhost:5000/api/summarize/pdf", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.error) {
          alert("❌ 요약 실패: " + data.error);
        } else {
          setText("📄 추출된 텍스트\n\n" + data.summary);
          summarizeText(data.summary);
        }
      } catch (err) {
        console.error("PDF 요청 실패:", err);
        alert("PDF 요약 중 오류 발생");
      } finally {
        setLoading(false);
      }
    } else if (["jpg", "jpeg", "png"].includes(ext)) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("mode", mode);

      try {
        setLoading(true);
        const response = await fetch("http://localhost:5000/api/summarize/image", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.error) {
          alert("❌ 요약 실패: " + data.error);
        } else {
          setText("📷 추출된 텍스트\n\n" + data.summary);
          summarizeText(data.summary);
        }
      } catch (err) {
        console.error("OCR 요청 실패:", err);
        alert("이미지 요약 중 오류 발생");
      } finally {
        setLoading(false);
      }
    } else {
      alert("지원되지 않는 파일 형식입니다.");
    }
  };

  return (
    <div className="mb-6 space-y-4">
      {/* 요약 길이 선택 */}
      <select
        className="select select-bordered w-full max-w-xs"
        value={mode}
        onChange={(e) => setMode(e.target.value)}
      >
        <option value="">자동 설정 (추천)</option>
        <option value="1문장">1문장 요약</option>
        <option value="3문장">3문장 요약</option>
        <option value="30%">30% 요약</option>
      </select>

      {/* 텍스트 입력 */}
      <textarea
        className="textarea textarea-bordered w-full"
        rows="6"
        placeholder="요약할 텍스트를 입력하세요"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      {/* 파일 업로드 */}
      <input
        type="file"
        accept=".txt,.md,.csv,.json,.pdf,.jpg,.jpeg,.png"
        onChange={handleFileChange}
        className="file-input file-input-bordered w-full max-w-xs"
      />

      {/* 로딩 메시지 */}
      {loading && <p className="text-sm text-gray-500">요약 중입니다...</p>}

      {/* 요약 실행 */}
      <button className="btn btn-primary" onClick={handleClick} disabled={loading}>
        요약 실행
      </button>
    </div>
  );
}
