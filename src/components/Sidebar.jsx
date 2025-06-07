// src/components/Sidebar.jsx
import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="menu p-4 w-56 min-h-screen bg-base-200">
      <ul className="menu menu-vertical">
        <li><Link to="/summary">문서 요약</Link></li>
        <li><Link to="/search">용어 검색</Link></li>
        <li><Link to="/history">이전 요약</Link></li>
      </ul>
    </div>
  );
}