import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";

function ProtectedRoute( {children} ) {
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    api.get("/auth/me")
    .then(() => setStatus("ok"))
    .catch(() => setStatus("unauth"));
    return
  }, []);
}

function Dashboard() {
  const logout = () => {
    await api.post("/auth/logout");
    navigate("/login");
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <button onClick={logout}>Log out</button>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}