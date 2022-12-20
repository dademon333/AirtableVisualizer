import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { AppRoute } from '../../const';
import { getSearchingElement } from '../../utils/get-searching-element';

type TableLinksProps = {
    setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const TableLinks = ({ setOpen }: TableLinksProps) => {
    const [query, setQuery] = useState<string>('');
    const currentPage = window.location.pathname;
    const initTables = [
        { name: 'Курс', to: `${AppRoute.Main}` },
        { name: 'Тема', to: `${AppRoute.Theme}` },
        { name: 'Знание', to: `${AppRoute.Knowledge}` },
        { name: 'Кванты знаний', to: `${AppRoute.Quantum}` },
        { name: 'Цель', to: `${AppRoute.Target}` }
    ];

    const tables = getSearchingElement({initData: initTables, query});
    
    return (
        <div className="table-links">
            <div className="search_tables">
                <input placeholder="Найти таблицу" onChange={event => setQuery(event.target.value)} />
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