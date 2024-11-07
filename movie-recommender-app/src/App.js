import "./App.css";
import Home from "./Pages/Home";
import SearchResult from "./Pages/SearchResult";
import Movie from "./Pages/Movie";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
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
                  <Route path="/movies" element={<Movie/>} />  
                </Routes>
            </Router>
        </div>
    );
}

export default App;
