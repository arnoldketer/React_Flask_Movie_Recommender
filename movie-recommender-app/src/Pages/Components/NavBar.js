// NavBar Component
import { Link } from "react-router-dom";
import "./styles/NavBarStyles.css";
import Logo from "./images/Logo2.png";

const NavBar = ({ isHome }) => {
    return (
        <div className="container header">
            <Link to="/">
                <img src={Logo} className="logo" alt="" />
            </Link>
            {/* If isHome is true, display the home button; otherwise, display the Movies button */}
            {isHome ? (
                <Link to="/" className="header-btn1 bouncy">
                    <i className="fas fa-home"></i> Home
                </Link>
            ) : (
                <Link to="/movies" className="header-btn1 bouncy">
                    <i className="fas fa-film"></i> Movies
                </Link>
            )}
        </div>
    );
};

export default NavBar;
