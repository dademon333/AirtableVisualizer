import React from "react";
import './Toolbar.css';

const Toolbar = ({ isSortingOptionsOpen, onSearchChange, onSortingClick, onSortingOptionClick, sortingOption }) => {
    return (
        <div className="toolbar">
            <div className="search">
                <img src="icons/search.svg" alt="search" />
                <input 
                    placeholder="Поиск" 
                    onChange={event => onSearchChange(event.target.value)}
                />
            </div>
            <div className={isSortingOptionsOpen ? "sorting opened" : "sorting"} 
                onClick={() => onSortingClick(!isSortingOptionsOpen)}
            >
                <div className="sorting_text"><img src="icons/sorting.svg" alt="sorting" />Сортировка</div>
                <div className={isSortingOptionsOpen ? "options" : "options closed"}>
                    <div className={sortingOption === 'default' ? "option clicked": "default"} onClick={() => onSortingOptionClick('default')}>По дате</div>
                    <div className={sortingOption === 'asc' ? "option clicked": "asc"} onClick={() => onSortingOptionClick('asc')}>
                        А <img src="icons/sorting_arrow.svg" alt="sorting_arrow" /> Я
                    </div>
                    <div className={sortingOption === 'desc' ? "option clicked": "desc"} onClick={() => onSortingOptionClick('desc')}>
                        Я <img src="icons/sorting_arrow.svg" alt="sorting_arrow" /> А
                    </div>
                </div> 
            </div>
        </div> 
    );
}

export default Toolbar;