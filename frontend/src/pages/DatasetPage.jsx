import { React, useState, useEffect } from "react";
import api from "../api";
import { useParams, useNavigate } from 'react-router-dom';
import Header from "../components/Header"
import Footer from "../components/Footer"
import DownloadButton from "../components/DownloadButton"
import TableWithClusters from "../components/TableWithClusters"
import "../styles/DatasetPage.css"

function DatasetPage() {

    const { id } = useParams();
    const [dataset, setDataset] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    const getDatasetDetails = (id) => {
        setLoading(true);
        api.get(`/datasets/${id}/`)
            .then((res) => res.data)
            .then((data) => {
                setDataset(data);
            })
            .catch((err) => alert(err))
            .finally(() => setLoading(false));
    };

    const deleteDataset = (id) => {
        api
            .delete(`/datasets/delete/${id}/`)
            .then((res) => {
                if (res.status !== 204) alert("Failed to delete dataset.");
                navigate('/');
            })
            .catch((error) => alert(error));
    };

    useEffect(() => {
        getDatasetDetails(id);
    }, [id]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="wrapper">
            <Header />
            <main>
                <div className="dataset-header">
                    <h1>{dataset.title}</h1>
                    <div className="buttons">
                        <DownloadButton dataset={dataset.clusters} />
                        <button className="delete-button" onClick={() => deleteDataset(dataset.id)}>Удалить</button>
                    </div>
                </div>
                <TableWithClusters dataset={dataset.clusters} />
            </main>
            <Footer />
        </div>
    );
}

export default DatasetPage;