import  { useState } from "react" ;
import { useNavigate, Link } from "react-router-dom" ;
import api from "../api/axios" ;

export default function Login() {
    const [form, setForm] = useState({"email": "", "password": ""});
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm({...form, [e.target.name]: e.target.value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try{
            const res = await api.post("/auth/login", form);
            navigate("/dashboard");
        } catch(err){
            setError(err.response?.data?.message || "Login failed :(");
        }
    };

    return(
        <div>
      <h2>Log in</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input name="email" placeholder="Email" onChange={handleChange} />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} />
        <button type="submit">Log in</button>
      </form>
      <p>No account? <Link to="/register">Register</Link></p>
    </div>
    );

}