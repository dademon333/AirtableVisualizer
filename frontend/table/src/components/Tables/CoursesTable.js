import React, { Component, useState } from "react";
import { Grid, Table, TableHeaderRow } from '@devexpress/dx-react-grid-bootstrap4';
import { SortingState, IntegratedSorting } from '@devexpress/dx-react-grid';
import { getChilds, getItems, wrapName, getSearchingElement } from '../../services/services';
import withData from '../withData';
import './tables.css';

const comparePriority = (a, b) => {
    if (a.props.children > b.props.children) {
        return 1;
    } else {
        return -1;
    }
};

const AddMenu = () => {
    const [isOpenAddMenu, setOpenAddMenu] = useState(false);
    const [query, setQuery] = useState("");
    const initMenuNames = [{ name: 'Тема'}];
    const menuNames = getSearchingElement(initMenuNames, query);

    return (
        <div className="add_container">
            <span className={isOpenAddMenu ? "add opened" : "add"} onClick={ () => setOpenAddMenu(!isOpenAddMenu) } />
            { isOpenAddMenu ?
                <div className="addMenu">
                    <div className="add_search">
                        <img src="icons/search_table.svg" alt="search" />
                        <input placeholder="Поиск" onChange={event => setQuery(event.target.value)} />
                    </div>
                    { menuNames.map((menuName, idx) => {
                        return (
                            <div className="addMenu_item checkMark" key={idx} onClick={() => setOpenAddMenu(false)}>{menuName.name}</div>
                        );
                    }) }
                </div>
            : null}
        </div>
    );
}

class CoursesTable extends Component {
    state = {
        query: "",
        columns: [
            { name: 'id', title: ' ' },
            { name: 'name', title: 'Название' },
            { name: 'themes', title: 'Тема' },
            { name: 'add', title: <AddMenu /> }
        ],
        tableColumnExtensions: [
            { columnName: 'id', width: '50px' },
            { columnName: 'name', width: '185px' },
            { columnName: 'themes', width: '980px' },
            { columnName: 'add', width: '65px' }
        ],
        integratedSortingColumnExtensions: [
            { columnName: 'name', compare: comparePriority }
        ],
        sortingStateColumnExtensions: [
            { columnName: 'id', sortingEnabled: false },
            { columnName: 'name', sortingEnabled: true },
            { columnName: 'themes', sortingEnabled: false },
            { columnName: 'add', sortingEnabled: false }
        ],
        isSortingOptionsOpen: false
    }

    setRows = () => {
        const {data} = this.props;
        const {query} = this.state;
        const rows = Object.entries(data.entities)
            .filter(entity => entity[1] !== undefined && entity[1].type === 'course')
            .filter(entity => {
                if (query === "") {
                    return entity; 
                } else if (entity[1].name.toLowerCase().trim().includes(query.toLowerCase().trim())) {
                    return entity;
                } else return null;
            })
            .map((entity, idx) => {
                const index = Number(entity[0]);
                const row = {};
                const childs = getChilds(data.connections[0], index);
                const themes = getItems(data.entities, childs, 'themeName');
                row.id = <div className="id">{idx + 1}</div>;
                row.name = wrapName(entity[1].name, 'courseName');
                row.themes = <div className="themes secondary-column-elements">{themes}</div>;
                return row;
        });
        return rows;
    }

    render() {
        const {columns, tableColumnExtensions, integratedSortingColumnExtensions, sortingStateColumnExtensions, isSortingOptionsOpen} = this.state;
        const rows = this.setRows();
        return (
            <div className='table_container courseTable'>
                <div className="toolbar">
                    <div className="search">
                        <img src="icons/search.svg" alt="search" />
                        <input 
                            placeholder="Поиск" 
                            onChange={event => this.setState({ query: event.target.value })}
                        />
                    </div>
                    <div className={this.state.isSortingOptionsOpen ? "sorting open" : "sorting"} 
                        onClick={() => this.setState({isSortingOptionsOpen: !this.state.isSortingOptionsOpen})}
                    >
                        <div className="sorting_text"><img src="icons/sorting.svg" alt="sorting" />Сортировка</div>
                        { isSortingOptionsOpen ?
                            <div className="options">
                                <div className="date">По дате</div>
                                <div className="asc">А <img src="icons/sorting_arrow.svg" alt="sorting_arrow" /> Я</div>
                                <div className="desc">Я <img src="icons/sorting_arrow.svg" alt="sorting_arrow" /> А</div>
                            </div> 
                        : null }
                    </div>
                </div> 
                <Grid
                    rows={rows}
                    columns={columns}
                >
                    <SortingState columnExtensions={sortingStateColumnExtensions} />
                    <IntegratedSorting columnExtensions={integratedSortingColumnExtensions} />
                    <Table columnExtensions={tableColumnExtensions} />
                    <TableHeaderRow showSortingControls />
                </Grid>
            </div>
        );
    }
}

export default withData(CoursesTable);