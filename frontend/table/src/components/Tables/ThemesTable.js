import React, { Component, useState } from "react";
import { Grid, Table, TableHeaderRow, TableColumnVisibility } from '@devexpress/dx-react-grid-bootstrap4';
import { getChilds, getItems, wrapName, getParents, getSearchingElement, comparePriority } from '../../services/services';
import withData from "../withData";
import Toolbar from "../Toolbar/Toolbar";
import './tables.css';

const AddMenu = ({ removeFromHiddenColumns }) => {
    const [isOpenAddMenu, setOpenAddMenu] = useState(false);
    const [query, setQuery] = useState("");
    const [clickedIds, setClickedId] = useState(['knowledges']);
    const initMenuNames = [
        { name: 'Знание', column: 'knowledges'},
        { name: 'Курс', column: 'course' }
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
                                setClickedId([...clickedIds, menuName.column]);
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

class ThemesTable extends Component {
    removeFromHiddenColumns = (column) => {
        const hiddenColumns = this.state.hiddenColumnNames;
        this.setState({ hiddenColumnNames: hiddenColumns.filter(e => e !== column) });
    }

    state = {
        query: "",
        columns: [
            { name: 'id', title: ' ' },
            { name: 'theme', title: 'Тема' },
            { name: 'knowledges', title: 'Знание' },
            { name: 'course', title: 'Курс' },
            { name: 'add', title: <AddMenu removeFromHiddenColumns={this.removeFromHiddenColumns} /> }
        ],
        tableColumnExtensions: [
            { columnName: 'id', width: '50px' },
            { columnName: 'theme', width: '300px' },
            { columnName: 'knowledges', width: '700px' },
            { columnName: 'course', width: '300px' },
            { columnName: 'add', width: '65px' }
        ],
        hiddenColumnNames: ['course'],
        isSortingOptionsOpen: false,
        sortingOption: 'default'
    }

    setRows = () => {
        const {data} = this.props;
        const {query, sortingOption} = this.state;
        const initData = Object.entries(data.entities)
            .filter(entity => entity[1] !== undefined && entity[1].type === 'theme');
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
                const childs = getChilds(data.connections[2], index);
                const knowledges = getItems(data.entities, childs, 'knowledgeName');
                parents.course = getParents(data.connections[0], index);
                const courseParent = getItems(data.entities, parents.course, 'course');
                row.course = <div className="courses secondary-column-elements">{courseParent}</div>;
                row.id = <div className="id">{idx + 1}</div>;
                row.theme = wrapName(entity[1].name, 'themeName');
                row.knowledges = <div className="knowledges secondary-column-elements">{knowledges}</div>;
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
            <div className='table_container themeTable'>
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

export default withData(ThemesTable);