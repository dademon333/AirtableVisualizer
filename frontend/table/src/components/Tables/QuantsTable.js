import React, { Component, useState } from "react";
import { Grid, Table, TableHeaderRow } from '@devexpress/dx-react-grid-bootstrap4';
import { getChilds, getItems, wrapName, getSearchingElement, comparePriority } from '../../services/services';
import withData from "../withData";
import Toolbar from "../Toolbar/Toolbar";
import './tables.css';

const AddMenu = () => {
    const [isOpenAddMenu, setOpenAddMenu] = useState(false);
    const [query, setQuery] = useState("");
    const initMenuNames = [{ name: 'Знание'}];
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

class QuantsTable extends Component {
    state = {
        query: "",
        columns: [
            { name: 'id', title: ' ' },
            { name: 'quantum', title: 'Квант' },
            { name: 'knowledges', title: 'Знание' },
            { name: 'add', title: <AddMenu /> }
        ],
        tableColumnExtensions: [
            { columnName: 'id', width: '50px' },
            { columnName: 'quantum', width: '200px' },
            { columnName: 'knowledges', width: '800px' },
            { columnName: 'add', width: '65px' }
        ],
        isSortingOptionsOpen: false,
        sortingOption: 'default'
    }
    
    setRows = () => {
        const {data} = this.props;
        const {query, sortingOption} = this.state;
        const initData = Object.entries(data.entities)
            .filter(entity => entity[1] !== undefined && entity[1].type === 'quantum');
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
                } else {
                    return null;
                }
            })
            .map((entity, idx) => {
                const index = Number(entity[0]);
                const row = {};
                const childs = getChilds(data.connections[6], index);
                const knowledges = getItems(data.entities, childs, 'knowledgeName');
                row.id = <div className="id">{idx + 1}</div>;
                row.quantum = wrapName(entity[1].name, 'quantumName');
                row.knowledges = <div className="knowledges secondary-column-elements">{knowledges}</div>;;
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
        const {columns, tableColumnExtensions, isSortingOptionsOpen, sortingOption} = this.state;
        const rows = this.setRows();
        return (
            <div className='table_container quantumTable'>
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
                    <Table columnExtensions={tableColumnExtensions} />
                    <TableHeaderRow />
                </Grid>
            </div>
        );
    }
}

export default withData(QuantsTable);