import React, { useState } from "react";
import { Link } from 'react-router-dom';
import './navigation.css';

const getTables = (initTables, query) => {
    return initTables.filter(table => {
        if (query === "") {
            return table;
        } else if (table.name.toLowerCase().trim().includes(query.toLowerCase().trim())) {
            return table;
        } else return null;
    });
}

const TableLinks = ({ setOpen }) => {
    const [query, setQuery] = useState("");
    const currentPage = window.location.pathname;
    const initTables = [
        { name: 'Курс', to: '/' },
        { name: 'Тема', to: '/theme' },
        { name: 'Знание', to: '/knowledge' },
        { name: 'Кванты знаний', to: '/quantum' },
        { name: 'Задание', to: '/task' }
    ];
    const tables = getTables(initTables, query);
    return (
        <div className="table-links">
            <div className="search_tables">
                <img src="icons/search_table.svg" alt="search" />
                <input placeholder="Найти таблицу" onChange={(event) => setQuery(event.target.value)} />
            </div>
            { tables.map((table, idx) => {
                return (
                    <Link 
                        to={table.to} 
                        className={table.to === currentPage ? 'table-link checkMark' : 'table-link'}
                        key={idx} 
                        onClick={() => setOpen(false)}
                    >
                        {table.name}
                    </Link>
                );
            }) }
        </div>
    );
}

export default TableLinks;