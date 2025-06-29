import React, { useState } from "react";
import Login from "./components/Login";
import RegistrationForm from "./components/RegistrationForm";
import Dashboard from "./components/Dashboard";

function App() {
  const [token, setToken] = useState("");
  const [page, setPage] = useState("login");

  const handleLogin = (token) => {
    setToken(token);
    setPage("dashboard");
  };

  return (
    <div>
      <nav style={{ display: "flex", gap: 10, padding: 10 }}>
        {token && <button onClick={() => setPage("dashboard")}>Dashboard</button>}
        {token && <button onClick={() => setPage("register")}>Register</button>}
        {!token && <button onClick={() => setPage("login")}>Login</button>}
        {token && <button onClick={() => { setToken(""); setPage("login"); }}>Logout</button>}
      </nav>
      {page === "login" && <Login onLogin={handleLogin} />}
      {page === "register" && <RegistrationForm token={token} />}
      {page === "dashboard" && <Dashboard token={token} />}
    </div>
  );
}

export default App;
