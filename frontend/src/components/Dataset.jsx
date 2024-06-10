import React from "react";
import "../styles/Dataset.css"
import { Link } from 'react-router-dom';
import DeleteImg from "../imgs/DeleteImg.svg";

function Dataset({ dataset, onDelete }) {
    const formattedDate = new Date(dataset.created_at).toLocaleDateString("ru")

    return (
        <div className="dataset-container">
            <div className="info-block">
                <Link className="dataset-link" to={`/dataset/${dataset.id}`}>{dataset.title}</Link>
                <p className="dataset-date">Создан: {formattedDate}</p>
            </div>
            <button className="delete-button" onClick={() => onDelete(dataset.id)}>
                <img src={DeleteImg} />
                <p>Удалить</p>
            </button>
        </div>
    );
}

export default Dataset