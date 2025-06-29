import React, { useState } from "react";
import { registerStudent } from "../api";

const initialState = {
  first_name: "",
  last_name: "",
  email: "",
  phone: "",
  date_of_birth: "",
  gender: "",
  address_line1: "",
  address_line2: "",
  city: "",
  state: "",
  postal_code: "",
  country: "",
  highest_education: "",
  institution_name: "",
  graduation_year: "",
  current_occupation: "",
  years_of_experience: "",
  previous_company: "",
  course_name: "",
  course_duration: "",
  preferred_batch_timing: "",
  preferred_start_date: "",
  how_did_you_hear: "",
  expectations: "",
  previous_programming_experience: false,
  programming_languages_known: ""
};

export default function RegistrationForm({ token, onSuccess }) {
  const [form, setForm] = useState(initialState);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(f => ({ ...f, [name]: type === "checkbox" ? checked : value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      await registerStudent(form, token);
      setSuccess("Registration successful!");
      setForm(initialState);
      if (onSuccess) onSuccess();
    } catch (err) {
      setError("Registration failed");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 600, margin: "2rem auto" }}>
      <h2>Student Registration</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
        <input name="first_name" placeholder="First Name" value={form.first_name} onChange={handleChange} required />
        <input name="last_name" placeholder="Last Name" value={form.last_name} onChange={handleChange} required />
        <input name="email" placeholder="Email" value={form.email} onChange={handleChange} required />
        <input name="phone" placeholder="Phone" value={form.phone} onChange={handleChange} required />
        <input name="date_of_birth" type="date" placeholder="Date of Birth" value={form.date_of_birth} onChange={handleChange} required />
        <input name="gender" placeholder="Gender" value={form.gender} onChange={handleChange} required />
        <input name="address_line1" placeholder="Address Line 1" value={form.address_line1} onChange={handleChange} required />
        <input name="address_line2" placeholder="Address Line 2" value={form.address_line2} onChange={handleChange} />
        <input name="city" placeholder="City" value={form.city} onChange={handleChange} required />
        <input name="state" placeholder="State" value={form.state} onChange={handleChange} required />
        <input name="postal_code" placeholder="Postal Code" value={form.postal_code} onChange={handleChange} required />
        <input name="country" placeholder="Country" value={form.country} onChange={handleChange} required />
        <input name="highest_education" placeholder="Highest Education" value={form.highest_education} onChange={handleChange} required />
        <input name="institution_name" placeholder="Institution Name" value={form.institution_name} onChange={handleChange} required />
        <input name="graduation_year" type="number" placeholder="Graduation Year" value={form.graduation_year} onChange={handleChange} />
        <input name="current_occupation" placeholder="Current Occupation" value={form.current_occupation} onChange={handleChange} />
        <input name="years_of_experience" type="number" placeholder="Years of Experience" value={form.years_of_experience} onChange={handleChange} />
        <input name="previous_company" placeholder="Previous Company" value={form.previous_company} onChange={handleChange} />
        <input name="course_name" placeholder="Course Name" value={form.course_name} onChange={handleChange} required />
        <input name="course_duration" placeholder="Course Duration" value={form.course_duration} onChange={handleChange} required />
        <input name="preferred_batch_timing" placeholder="Preferred Batch Timing" value={form.preferred_batch_timing} onChange={handleChange} required />
        <input name="preferred_start_date" type="date" placeholder="Preferred Start Date" value={form.preferred_start_date} onChange={handleChange} required />
        <input name="how_did_you_hear" placeholder="How did you hear?" value={form.how_did_you_hear} onChange={handleChange} />
        <input name="expectations" placeholder="Expectations" value={form.expectations} onChange={handleChange} />
        <label>
          Previous Programming Experience
          <input name="previous_programming_experience" type="checkbox" checked={form.previous_programming_experience} onChange={handleChange} />
        </label>
        <input name="programming_languages_known" placeholder="Programming Languages Known" value={form.programming_languages_known} onChange={handleChange} />
      </div>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {success && <div style={{ color: "green" }}>{success}</div>}
      <button type="submit">Submit</button>
    </form>
  );
}