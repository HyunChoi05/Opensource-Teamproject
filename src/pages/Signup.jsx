// src/pages/Signup.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const navigate = useNavigate();

  const handleSignup = (e) => {
    e.preventDefault();

    if (password !== confirm) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    const users = JSON.parse(localStorage.getItem("users") || "[]");
    const exists = users.some((u) => u.email === email);
    if (exists) {
      alert("이미 가입된 이메일입니다.");
      return;
    }

    const updated = [...users, { email, password }];
    localStorage.setItem("users", JSON.stringify(updated));

    alert("회원가입 성공!");
    navigate("/login");
  };

  return (
    <div className="max-w-sm mx-auto mt-10 p-6 bg-base-100 shadow-md rounded">
      <h2 className="text-xl font-bold mb-4">회원가입</h2>
      <form onSubmit={handleSignup} className="space-y-4">
        <input
          type="email"
          placeholder="이메일"
          className="input input-bordered w-full"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="비밀번호"
          className="input input-bordered w-full"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          placeholder="비밀번호 확인"
          className="input input-bordered w-full"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
        />
        <button type="submit" className="btn btn-primary w-full">회원가입</button>
      </form>
    </div>
  );
}
