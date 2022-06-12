import React, { Component, useState } from "react";
import { Grid, Table, TableHeaderRow, TableColumnVisibility } from '@devexpress/dx-react-grid-bootstrap4';
import { getChilds, getItems, wrapName, getParents, getSearchingElement, comparePriority } from '../../services/services';
import withData from "../withData";
import Toolbar from "../Toolbar/Toolbar";
import './tables.css';

const AddMenu = ({ removeFromHiddenColumns }) => {
    const [isOpenAddMenu, setOpenAddMenu] = useState(false);
    const [query, setQuery] = useState("");
    const [clickedIds, setClickedId] = useState('theme');
    const initMenuNames = [
        { name: 'Тема', column: 'theme' },
        { name: 'Цель', column: 'target'},
        { name: 'Квант', column: 'quantum' }
    ];
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
                            <div className={clickedIds.includes(menuName.column) ? "addMenu_item checkMark" : "addMenu_item"} key={idx} onClick={() => {
                                setClickedId(menuName.column);
                                removeFromHiddenColumns(menuName.column);
                                setOpenAddMenu(false);
                            }}>{menuName.name}</div>
                        );
                    }) }
                </div>
            : null}
        </div>
    );
}

class KnowledgesTable extends Component {
    removeFromHiddenColumns = (column) => {
        if (column === 'theme') {
            this.setState({ hiddenColumnNames: ['quantum', 'target'] });
        } else if (column === 'quantum') {
            this.setState({ hiddenColumnNames: ['theme', 'target'] });
        } else if (column === 'target') {
            this.setState({ hiddenColumnNames: ['quantum', 'theme'] });
        }
    }

    state = {
        query: "",
        columns: [
            { name: 'id', title: ' ' },
            { name: 'knowledge', title: 'Знание' },
            { name: 'theme', title: 'Тема' },
            { name: 'target', title: 'Цель' },
            { name: 'quantum', title: 'Квант' },
            { name: 'add', title: <AddMenu removeFromHiddenColumns={this.removeFromHiddenColumns} /> }
        ],
        tableColumnExtensions: [
            { columnName: 'id', width: '50px' },
            { columnName: 'knowledge', width: '500px' },
            { columnName: 'theme', width: '700px' },
            { columnName: 'target', width: '400px' },
            { columnName: 'quantum', width: '400px' },
            { columnName: 'add', width: '65px' }
        ],
        hiddenColumnNames: ['target', 'quantum'],
        isSortingOptionsOpen: false,
        sortingOption: 'default'
    }
    
    setRows = () => {
        const {data} = this.props;
        const {query, sortingOption} = this.state;
        const initData = Object.entries(data.entities)
            .filter(entity => entity[1] !== undefined && entity[1].type === 'knowledge');
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
                const parents = {};
                const childsTarget = getChilds(data.connections[3], index);
                const target = getItems(data.entities, childsTarget, 'targetName');
                parents.theme = getParents(data.connections[2], index);
                parents.quantum = getParents(data.connections[6], index);
                const themeParent = getItems(data.entities, parents.theme, 'theme');
                const quantumParent = getItems(data.entities, parents.quantum, 'quantum');
                row.id = <div className="id">{idx + 1}</div>;
                row.knowledge = wrapName(entity[1].name, 'knowledgeName');
                row.target = <div className="targets secondary-column-elements">{target}</div>;
                row.quantum = <div className="quantums secondary-column-elements">{quantumParent}</div>;
                row.theme = <div className="themes secondary-column-elements">{themeParent}</div>;
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
        const {columns, tableColumnExtensions, hiddenColumnNames, isSortingOptionsOpen, sortingOption} = this.state;
        const rows = this.setRows();
        return (
            <div className='table_container knowledgeTable'>
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
                    <TableColumnVisibility hiddenColumnNames={hiddenColumnNames} />
                </Grid>
            </div>
        );
    }
}

export default withData(KnowledgesTable);