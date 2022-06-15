import React from "react";
import './Toolbar.css';
import '../../icons/search.svg';
import { ReactComponent as SearchIcon } from '../../icons/search.svg';
import { ReactComponent as SortingIcon } from '../../icons/sorting.svg';
import { ReactComponent as SortingArrowIcon } from '../../icons/sorting_arrow.svg';

const Toolbar = ({ isSortingOptionsOpen, onSearchChange, onSortingClick, onSortingOptionClick, sortingOption }) => {
    return (
        <div className="toolbar">
            <div className="search">
                <SearchIcon />
                <input 
                    placeholder="Поиск" 
                    onChange={event => onSearchChange(event.target.value)}
                />
            </div>
            <div className={isSortingOptionsOpen ? "sorting opened" : "sorting"} 
                onClick={() => onSortingClick(!isSortingOptionsOpen)}
            >
                <div className="sorting_text"><SortingIcon />Сортировка</div>
                <div className={isSortingOptionsOpen ? "options" : "options closed"}>
                    <div className={sortingOption === 'default' ? "option clicked": "default"} onClick={() => onSortingOptionClick('default')}>По дате</div>
                    <div className={sortingOption === 'asc' ? "option clicked": "asc"} onClick={() => onSortingOptionClick('asc')}>
                        А <SortingArrowIcon /> Я
                    </div>
                    <div className={sortingOption === 'desc' ? "option clicked": "desc"} onClick={() => onSortingOptionClick('desc')}>
                        Я <SortingArrowIcon /> А
                    </div>
                </div> 
            </div>
        </div> 
    );
}

export default Toolbar;