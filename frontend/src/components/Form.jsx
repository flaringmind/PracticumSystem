import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css"
import LoadingIndicator from "./LoadingIndicator";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Вход" : "Регистрация";
    const buttonName = method === "login" ? "Войти" : "Зарегистрироваться";


    const handleToLoginClick = () => {
        navigate('/login');
      };
    
    const handleToRegistrationClick = () => {
        navigate('/register');
    };

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post(route, { username, password })
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                localStorage.setItem('username', username);
                navigate("/")
            } else {
                navigate("/login")
            }
        } catch (error) {
            //alert(error)
        } finally {
            setLoading(false)
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{name}</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Имя пользователя"
            />
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Пароль"
            />
            {loading ?
            (<LoadingIndicator />) :
            (<button className="form-button" type="submit">{buttonName}</button>)
            }
            <div className="redirect-block">
                <p>{method === "login" ? "Ещё нет аккаунта? " : "Уже зарегистрированы? "}</p>
                <p className="redirect"
                    onClick={method === "login" ? handleToRegistrationClick : handleToLoginClick}>
                    {method === "login" ?  "Зарегистрируйтесь" : "Войдите"}
                </p>
            </div>
        </form>
    );
}

export default Form