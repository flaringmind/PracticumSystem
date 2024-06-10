import React from 'react';
import { useNavigate } from 'react-router-dom';
import "../styles/Header.css";
import Logo from "../imgs/Logo.svg";
import LogoutImg from "../imgs/LogoutImg.svg";

const Header = () => {
  
    const navigate = useNavigate();
    const storedUsername = localStorage.getItem('username');

    const handleLogoClick = () => {
        navigate('/');
    };

    const handleLogoutClick = () => {
        navigate('/logout');
    };

    return (
        <header>
            <div className="header-container">
                <div className="logo" onClick={handleLogoClick}>
                    <img src={Logo} alt="Logo" />
                </div>
                <div className="user-info">
                    <p>{storedUsername}</p>
                    <div className="logout-button" onClick={handleLogoutClick}>
                       <img src={LogoutImg} alt="Logout" />
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;