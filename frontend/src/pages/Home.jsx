import { useState, useEffect } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom"
import Dataset from "../components/Dataset"
import Header from "../components/Header"
import Footer from "../components/Footer"
import "../styles/Home.css"

function Home() {
    const [datasets, setDatasets] = useState([]);
    const navigate = useNavigate();
    
    useEffect(() => {
        getDatasets();
    }, []);

    const getDatasets = () => {
        api.get("/datasets/")
            .then((res) => res.data)
            .then((data) => {
                setDatasets(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

    const deleteDataset = (id) => {
        api
            .delete(`/datasets/delete/${id}/`)
            .then((res) => {
                if (res.status !== 204) alert("Failed to delete dataset.");
                getDatasets();
            })
            .catch((error) => alert(error));
    };

    const handleCreateByIdClick = () => {
        navigate('/create');
    };

    return (
        <div className="wrapper">
            <Header />
            <main>
                <div className="dataset-create">
                    <h1>Новый датасет</h1>
                    <p>Добро пожаловать в систему интеллектуального анализа потребностей рынка труда. 
                        Анализ производится посредством получения датасетов, содержащих 
                        требования из вакансий системы онлайн–рекрутмента HeadHunter, 
                        сгруппированными в кластеры по тематикам. На основе возможных названий 
                        профессий, получаемых из содержания профессиональных стандартов, 
                        производится поиск и извлечение требований 
                        из описаний вакансий, их обработка и кластеризация.</p>
                    <button className="home-create-button" onClick={handleCreateByIdClick}>
                        Создать датасет
                    </button>
                </div>

                <div className="datasets-block">
                    {datasets
                    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                    .map((dataset) => (
                        <Dataset dataset={dataset} onDelete={deleteDataset} key={dataset.id} />
                    ))}
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Home;