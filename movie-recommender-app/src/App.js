import "./App.css";
import Home from "./Pages/Home";
import SearchResult from "./Pages/SearchResult";
import Movie from "./Pages/Movie";
import Register from "./Pages/Register";
import Login from "./Pages/Login";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";

function App() {
    const [accessToken, setAccessToken] = useState("");
    const [userId, setUserId] = useState("");

    return (
        <div className="App">
            <Router>
                <Routes>
                    <Route exact path="/" element={<Home />} />
                    <Route
                        exact
                        path="/search/:id"
                        element={<SearchResult />}
                    />
                    <Route path="/movies" element={<Movie />} />
                    <Route path="/register" element={<Register />} />
                    {/* Pass setAccessToken and setUserId as props */}
                    <Route
                        path="/login"
                        element={
                            <Login
                                setAccessToken={setAccessToken}
                                setUserId={setUserId}
                            />
                        }
                    />
                </Routes>
            </Router>
        </div>
    );
}


export default App;
