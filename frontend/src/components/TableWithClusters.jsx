import ReactPaginate from 'react-paginate';
import React, { useState } from 'react';
import {useNavigate } from 'react-router-dom';

const TableWithClusters = ({ dataset }) => {
    const [currentPage, setCurrentPage] = useState(0);
    const navigate = useNavigate();

    const pageSize = 15;

    const offset = currentPage * pageSize;
    const currentData = dataset.slice(offset, offset + pageSize);
    const pageCount = Math.ceil(dataset.length / pageSize);

    const handlePageClick = ({ selected }) => {
        setCurrentPage(selected);
    };

    const handleCancelClick = () => {
        navigate('/');
    };

    return (
        <div className="table-container">
            <table>
                <thead>
                    <tr>
                        <th style={{ width: '50px' }}>Номер кластера</th>
                        <th>Ключевые навыки</th>
                    </tr>
                </thead>
                <tbody>
                    {currentData.map((cluster, index) => (
                        <tr key={index}>
                            <td style={{ textAlign: 'center' }}>{index + offset + 1}</td>
                            <td className="truncate">{cluster}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="table-footer">
                <div className="left-block"></div>
                <ReactPaginate
                    previousLabel={'<'}
                    nextLabel={'>'}
                    breakLabel={'...'}
                    pageCount={pageCount}
                    marginPagesDisplayed={1}
                    pageRangeDisplayed={1}
                    onPageChange={handlePageClick}
                    containerClassName={'pagination'}
                    activeClassName={'active'}
                />
                <button className="back-button" onClick={handleCancelClick}>Назад</button>
            </div>
        </div>
    );
};

export default TableWithClusters;