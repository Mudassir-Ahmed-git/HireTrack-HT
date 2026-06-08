import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/axios" ;

export default function Register() {
    const [form, setForm] = useState({"username": "", "email": "", "password": ""});
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm({...form, [e.target.name]: e.target.value});   
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try{
            await api.post("/auth/register", form);
            navigate("/login");
        } catch(err){
            setError(err.response?.data?.message || "Registraton failed :(");
        }
    }

    return (
    <div>
      <h2>Create account</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input name="email" placeholder="Email" onChange={handleChange} />
        <input name="username" placeholder="Username" onChange={handleChange} />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} />
        <button type="submit">Register</button>
      </form>
      <p>Already have an account? <Link to="/login">Log in</Link></p>
    </div>
  );
  
}