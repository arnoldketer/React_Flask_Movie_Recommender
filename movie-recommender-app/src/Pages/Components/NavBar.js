// NavBar Component
import { Link } from "react-router-dom";
import "./styles/NavBarStyles.css";
import Logo from "./images/movielogo.png";


const NavBar = ({ isHome }) => {
  return (
    <div className="container header">
      <Link to="/">
        <img src={Logo} className="logo" alt="Logo" />
      </Link>
      <nav className="nav-links">
        <Link to="/" className={`header-btn ${isHome ? "active" : ""}`}>
          <i className="fas fa-home"></i> Home
        </Link>
        <Link to="/movies" className="header-btn">
          <i className="fas fa-film"></i> Movies
        </Link>
        <Link to="/register" className="header-btn">
          <i className="fas fa-user-plus"></i> Register
        </Link>
        <Link to="/login" className="header-btn">
          <i className="fas fa-sign-in-alt"></i> Login
        </Link>
      </nav>
    </div>
  );
};

export default NavBar;
