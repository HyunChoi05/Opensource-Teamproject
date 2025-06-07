import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Home from "./pages/Home";
import Summary from "./pages/Summary";
import TermSearch from "./pages/TermSearch";
import History from "./pages/History";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import PrivateRoute from "./PrivateRoute";

function App() {
  return (
    <Routes>
      {/* 홈 기반 내부 구조 */}
      <Route path="/" element={<Home />}>
        <Route index element={<Navigate to="/summary" replace />} />
        <Route
          path="summary"
          element={<PrivateRoute><Summary /></PrivateRoute>}
        />
        <Route
          path="search"
          element={<PrivateRoute><TermSearch /></PrivateRoute>}
        />
        <Route
          path="history"
          element={<PrivateRoute><History /></PrivateRoute>}
        />
      </Route>

      {/* 로그인 / 회원가입 외부 페이지 */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
    </Routes>
  );
}

export default App;
