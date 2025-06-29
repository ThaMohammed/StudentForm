import React, { useEffect, useState } from "react";
import { getRegistrations } from "../api";

export default function Dashboard({ token }) {
  const [registrations, setRegistrations] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getRegistrations(token);
        setRegistrations(data);
      } catch (err) {
        setError("Failed to load registrations");
      }
    }
    if (token) fetchData();
  }, [token]);

  if (!token) return <div>Please login to view your dashboard.</div>;

  return (
    <div style={{ maxWidth: 900, margin: "2rem auto" }}>
      <h2>Dashboard</h2>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <table border="1" cellPadding="5" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Course</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {registrations.map(reg => (
            <tr key={reg.id}>
              <td>{reg.first_name}</td>
              <td>{reg.last_name}</td>
              <td>{reg.email}</td>
              <td>{reg.course_name}</td>
              <td>{reg.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}