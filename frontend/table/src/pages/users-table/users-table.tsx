import { useState } from 'react';
import { PagingState, IntegratedPaging, SelectionState, IntegratedSelection } from '@devexpress/dx-react-grid';
import { Grid, Table, TableHeaderRow, TableSelection } from '@devexpress/dx-react-grid-bootstrap4';
import { PagingPanel } from '@devexpress/dx-react-grid-material-ui';
import { useAppSelector } from '../../hooks';
import Navigation from '../../components/navigation/navigation';
import Toolbar from '../../components/tool-bar/tool-bar';
import { getRows, getColumns } from '../../redux/users-page-data/selectors';
import { setRows } from '../../utils/set-rows';
import { messages } from '../../const';

const UsersTable = (): JSX.Element => {
  const columnExtensions: Table.ColumnExtension[] = [{
    columnName: 'id',
    width: '100px'
  }, {
    columnName: 'name',
    width: '100px'
  }, {
    columnName: 'email',
    width: '120px'
  }, {
    columnName: 'status',
    width: '150px'
  }, {
    columnName: 'created',
    width: '700px'
  }];

  const rows = useAppSelector(getRows);
  const columns = useAppSelector(getColumns);

  const [query, setQuery] = useState<string>('');
  const [selection, setSelection] = useState<(number | string)[]>([]);

  return (
    <>
      <Navigation />
      <Toolbar onSearchChange={setQuery} />
      {
        <div className='table_container coursesTable'>
          <Grid
            rows={setRows(rows, query)}
            columns={columns}
          >
            <SelectionState selection={selection} onSelectionChange={setSelection} />
            <IntegratedSelection />
            <PagingState defaultCurrentPage={0} defaultPageSize={10} />
            <IntegratedPaging />
            <Table columnExtensions={columnExtensions} />
            <PagingPanel pageSizes={[5, 10, 15, 0]} messages={messages} />
            <TableHeaderRow />
            <TableSelection showSelectAll />
          </Grid>
        </div>
      }
    </>
    );
}

export default UsersTable;
