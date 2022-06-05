import React, { Component } from "react";
import { Grid, Table, TableHeaderRow, TableSelection } from '@devexpress/dx-react-grid-bootstrap4';
import { SelectionState, IntegratedSelection } from '@devexpress/dx-react-grid';
import { getChilds, getItems, wrapName, addLabels } from '../../services/services';
import withData from "../withData";
import './tables.css';

class QuantsTable extends Component {
    state = {
        query: "",
        columns: [
            { name: 'id', title: ' ' },
            { name: 'quantum', title: 'Квант' },
            { name: 'knowledges', title: 'Знания' },
            { name: 'add', title: <span className="add" /> }
        ],
        selection: [],
        tableColumnExtensions: [
            { columnName: 'id', width: '50px' },
            { columnName: 'quantum', width: '200px' },
            { columnName: 'knowledges', width: '750px' },
            { columnName: 'add', width: '65px' }
        ]
    }
    
    setRows = () => {
        const {data} = this.props;
        const {query} = this.state;
        const rows = Object.entries(data.entities)
            .filter(entity => entity[1] !== undefined && entity[1].type === 'quantum')
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
                const childs = getChilds(data.connections[7], index);
                const knowledges = getItems(data.entities, childs, 'knowledgeName');
                row.id = <div className="id">{idx + 1}</div>;
                row.quantum = wrapName(entity[1].name, 'quantumName');
                row.knowledges = <div className="knowledges secondary-column-elements">{knowledges}</div>;;
                return row;
        });
        addLabels();
        return rows;
    }

    render() {
        const {columns, selection, tableColumnExtensions} = this.state;
        const rows = this.setRows();
        return (
            <div className='table_container quantumsTable'>
                <div className="toolbar">
                    <div className="search">
                        <img src="icons/search.svg" alt="search" />
                        <input 
                            placeholder="Поиск" 
                            onChange={event => this.setState({ query: event.target.value })}
                        />
                    </div>
                </div> 
                <Grid
                    rows={rows}
                    columns={columns}
                >
                    <SelectionState 
                        selection={selection}
                        onSelectionChange={selected => this.setState({ selection: selected })}
                    />
                    <IntegratedSelection />
                    <Table columnExtensions={tableColumnExtensions} />
                    <TableHeaderRow />
                    <TableSelection selectionColumnWidth={0} />
                </Grid>
            </div>
        );
    }
}

export default withData(QuantsTable);