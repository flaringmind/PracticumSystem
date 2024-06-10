import React from 'react';

const DownloadButton = ({ dataset }) => {

    const convertToCSV = (array) => {
        const csvRows = [];
        csvRows.push("cluster;skills");
        array.forEach((item, index) => {
            csvRows.push(`${index + 1};${item}`);
        });
        return csvRows.join('\n');
    };

    const handleDownload = () => {
        const csv = convertToCSV(dataset);
        const bom = "\uFEFF"; // UTF-8 BOM
        const csvWithBom = bom + csv;

        // Создание блоба и ссылки для скачивания
        const blob = new Blob([csvWithBom], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'dataset.csv');

        // Программа нажатия на ссылку
        document.body.appendChild(link);
        link.click();

        // Удаление ссылки после скачивания
        document.body.removeChild(link);
    };

    return (
        <button className="download-button" onClick={handleDownload}>Скачать в CSV</button>
    );
};

export default DownloadButton;