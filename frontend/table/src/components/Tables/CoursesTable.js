import React, { Component, useState } from "react";
import { PagingState, IntegratedPaging } from '@devexpress/dx-react-grid';
import { Grid, Table, TableHeaderRow } from '@devexpress/dx-react-grid-bootstrap4';
import { PagingPanel } from '@devexpress/dx-react-grid-material-ui';
import { getChilds, getItems, wrapName, getSearchingElement, comparePriority } from '../../services/services';
import withData from '../withData';
import Toolbar from "../Toolbar/Toolbar";
import './tables.css';
import { ReactComponent as SearchTableIcon } from '../../icons/search_table.svg';


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
                        <SearchTableIcon />
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
        isSortingOptionsOpen: false,
        sortingOption: 'default',
        pageSizes: [5, 10, 15, 0]
    }

    setRows = () => {
        const {data} = this.props;
        const {query, sortingOption} = this.state;
        const initData = Object.entries(data.entities)
            .filter(entity => entity[1] !== undefined && entity[1].type === 'course');
        const sortedData = 
            sortingOption === 'default' ? initData :
            sortingOption === 'asc' ? initData.sort((entity1, entity2) => comparePriority(entity1[1].name, entity2[1].name)) :
            sortingOption === 'desc' ? initData.sort((entity1, entity2) => comparePriority(entity2[1].name, entity1[1].name)) : null;
        const rows = sortedData
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

    onSearchChange = (value) => {
        this.setState({ query: value });
    }

    onSortingClick = (value) => {
        this.setState({ isSortingOptionsOpen: value });
    }

    onSortingOptionClick = (value) => {
        this.setState({ sortingOption: value });
    }

    render() {
        const {columns, tableColumnExtensions, isSortingOptionsOpen, sortingOption, pageSizes} = this.state;
        const rows = this.setRows();
        const messages = {showAll: 'Все', rowsPerPage: 'Строк на странице:', info: '{from}-{to} из {count}'};
        return (
            <div className='table_container courseTable'>
                <Toolbar 
                    isSortingOptionsOpen={isSortingOptionsOpen}
                    onSearchChange={this.onSearchChange}
                    onSortingClick={this.onSortingClick}
                    onSortingOptionClick={this.onSortingOptionClick}
                    sortingOption={sortingOption}  
                />
                <Grid
                    rows={rows}
                    columns={columns}
                >
                    <PagingState defaultCurrentPage={0} defaultPageSize={10} />
                    <IntegratedPaging />
                    <Table columnExtensions={tableColumnExtensions} />
                    <PagingPanel pageSizes={pageSizes} messages={messages} />
                    <TableHeaderRow />
                </Grid>
            </div>
        );
    }
}

export default withData(CoursesTable);