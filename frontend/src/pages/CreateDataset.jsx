import { useState } from "react";
import { useNavigate } from 'react-router-dom';
import api from "../api";
import "../styles/CreateDataset.css"
import Header from "../components/Header"
import Footer from "../components/Footer"
import LoadingIndicator from "../components/LoadingIndicator";

function CreateDataset() {

    const [title, setTitle] = useState("");
    const [profStandart, setProfStandart] = useState("");
    const [findByCode, setFindByCode] = useState(true);
    const [checkedBox, setCheckedBox] = useState('box1');

    const [pslist, setPslist] = useState("");
    const [profession, setProfession] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleCancelClick = () => {
        navigate('/');
    };

    const handleCheckboxChange = (box) => {
        if (checkedBox !== box) {
          setFindByCode(!findByCode);
          setCheckedBox(box);
        } 
    };

    const createDataset = (e) => {
        e.preventDefault();
        setLoading(true);
        api
            .post("/create/", { title, profStandart, findByCode })
            .then((res) => {
                if (res.status === 201) {
                    setPslist(res.data);
                }
                else alert("Failed to make dataset.");
            })
            .catch((err) => alert(err))
            .finally(() => setLoading(false));
    };

    const findVacancies = (e, dataset_id) => {
        e.preventDefault();
        setLoading(true);
        api
            .post("/find/", { profession, dataset_id })
            .then((res) => {
                if (res.status === 200) {
                    navigate(`/dataset/${dataset_id}`);
                }
                else alert("Failed to make dataset.");
            })
            .catch((err) => alert(err))
            .finally(() => setLoading(false));
    };

    return (
        <div className="wrapper">
            <Header />
            <main>
                <div className="create-container">
                    <h1>Создание датасета</h1>
                    {pslist === "" ? (
                    <form onSubmit={createDataset}>
                        <p className="create-info">В качестве исходных данных для получения датасета могут 
                            использоваться названия профессий как из одного профессионального 
                            стандарта, найденного по его кодовому номеру, 
                            так и из нескольких профессиональных стандартов, 
                            найденных по наименованию:
                        </p>
                        <div className="checkbox-container">
                            <div className="checkbox">
                                <input
                                        type="checkbox"
                                        checked={checkedBox === 'box1'}
                                        onChange={() => handleCheckboxChange('box1')}
                                    />
                                <label>Найти по номеру</label>
                            </div>
                            <div className="checkbox">
                                <input
                                        type="checkbox"
                                        checked={checkedBox === 'box2'}
                                        onChange={() => handleCheckboxChange('box2')}
                                    />
                                <label>Найти по наименованию</label>
                            </div>
                        </div>
                        <br />

                        <label htmlFor="title">Название нового датасета:</label>
                        <br />
                        <input
                            type="text"
                            id="title"
                            name="title"
                            required
                            onChange={(e) => setTitle(e.target.value)}
                            value={title}
                        />
                        <br />
                        {findByCode ?
                        (<label htmlFor="profStandart">Номер профессионального стандарта:</label>) :
                        (<label htmlFor="profStandart">Наименование для профессиональных стандартов:</label>)}
                        <br />
                        <input
                            type="text"
                            id="profStandart"
                            name="profStandart"
                            required
                            onChange={(e) => setProfStandart(e.target.value)}
                            value={profStandart}
                        />
                        <br />

                        {loading ?
                        (<div className="create-loader">
                            <LoadingIndicator />
                            <p>Пожалуйста подождите. Загрузка профессиональных 
                                стандартов может занять некоторое время...</p>
                        </div>) :
                        (<div className="buttons">
                            <input className="find-button" type="submit" value="Поиск"></input>
                            <button className="back-button" onClick={handleCancelClick}>Назад</button>
                        </div>)}
                    </form>
                    ) : (
                        <>
                            <div className="profstandart-list">
                                <h2>По вашему запросу были найдены возможные названия профессий:</h2>
                                {pslist.pslist.map(ps => (
                                    <>
                                        <p>{ps.code} {ps.name}</p>
                                        <ol>{ps.job_titles.map(jobTitle => (
                                        <li>{jobTitle}</li>
                                        ))}</ol>
                                    </>
                                ))}
                            </div>
                            <br />

                            <form onSubmit={(e) => findVacancies(e, pslist.dataset_id)}>
                                <label htmlFor="profession">Введите название профессии:</label>
                                <br />
                                <input
                                    type="text"
                                    id="profession"
                                    name="profession"
                                    required
                                    onChange={(e) => setProfession(e.target.value)}
                                    value={profession}
                                />
                                <br />
                                {loading ?
                                (<div className="create-loader">
                                    <LoadingIndicator />
                                    <p>Пожалуйста подождите. Загрузка данных из вакансий 
                                         может занять некоторое время...</p>
                                </div>) :
                                (<div className="buttons">
                                    <input className="find-button" type="submit" value="Поиск"></input>
                                    <button className="back-button" onClick={handleCancelClick}>Назад</button>
                                </div>)}
                            </form>
                        </>
                    )}
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default CreateDataset;