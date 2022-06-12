import React, { Component, useState } from "react";
import { Grid, Table, TableHeaderRow } from '@devexpress/dx-react-grid-bootstrap4';
import { wrapName, getParents, getItems, getChilds, comparePriority } from '../../services/services';
import withData from "../withData";
import Toolbar from "../Toolbar/Toolbar";
import './tables.css';

const AddMenu = () => {
    const [isOpenAddMenu, setOpenAddMenu] = useState(false);

    return (
        <div className="add_container">
            <span className={isOpenAddMenu ? "add opened" : "add"} onClick={ () => setOpenAddMenu(!isOpenAddMenu) } />
            { isOpenAddMenu ?
                <div className="addMenu" style={{"fontSize": "14px", "padding": "10px"}}>
                    Здесь пока ничего нет
                </div>
            : null}
        </div>
    );
}

class TasksTable extends Component {
    state = {
        query: "",
        columns: [
            { name: 'id', title: ' ' },
            { name: 'task', title: 'Задание' },
            { name: 'target', title: 'Цель'},
            { name: 'activity', title: 'Активность' },
            { name: 'add', title: <AddMenu removeFromHiddenColumns={this.removeFromHiddenColumns} /> }
        ],
        tableColumnExtensions: [
            { columnName: 'id', width: '50px' },
            { columnName: 'task', width: '600px' },
            { columnName: 'target', width: '200px' },
            { columnName: 'activity', width: '200px' },
            { columnName: 'add', width: '65px' }
        ],
        isSortingOptionsOpen: false,
        sortingOption: 'default'
    }

    setRows = () => {
        const {data} = this.props;
        const {query, sortingOption} = this.state;
        const initData = Object.entries(data.entities)
            .filter(entity => entity[1] !== undefined && entity[1].type === 'task');
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
                const targetParent = getParents(data.connections[5], index);
                const target = getItems(data.entities, targetParent, 'target');
                const childActivity = getChilds(data.connections[4], targetParent[0]);
                const activity = getItems(data.entities, childActivity, 'activity');
                row.id = <div className="id">{idx + 1}</div>;
                row.task = wrapName(entity[1].name, 'taskName');
                row.target = <div className="targets secondary-column-elements">{target}</div>
                row.activity = <div className="activities secondary-column-elements">{activity}</div>
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
            <div className='table_container taskTable'>
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

export default withData(TasksTable);