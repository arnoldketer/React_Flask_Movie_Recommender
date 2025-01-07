import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import for navigation

const Login = ({ setAccessToken, setUserId }) => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // Use navigate for redirection

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(""); // Clear previous messages

    try {
      const response = await fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Response data:", data);

        // Save token to localStorage
        localStorage.setItem("token", data.access_token);

        // Update parent state
        setAccessToken(data.access_token);
        setUserId(data.userId);

        setMessage("Login successful!");
        
        // Redirect to home page or protected route
        navigate("/");
      } else {
        const errorData = await response.json();
        setMessage(errorData.error || "Login failed. Please try again.");
      }
    } catch (error) {
      console.error("Fetch error:", error);
      setMessage("An error occurred during login. Please check your connection.");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Login;

