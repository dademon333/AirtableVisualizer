import { useEffect, useState } from 'react';
import { PagingState, IntegratedPaging, SelectionState, IntegratedSelection } from '@devexpress/dx-react-grid';
import { Grid, Table, TableHeaderRow, TableSelection } from '@devexpress/dx-react-grid-bootstrap4';
import { PagingPanel } from '@devexpress/dx-react-grid-material-ui';
import Spinner from 'react-bootstrap/Spinner';
import { useAppDispatch } from '../../hooks';
import { useAppSelector } from '../../hooks';
import { fetchKnowledges } from '../../redux/knowledges-data/api-actions';
import Navigation from '../../components/navigation/navigation';
import Toolbar from '../../components/tool-bar/tool-bar';
import { getRows, getColumns, getIsLoading } from '../../redux/knowledges-data/selectors';
import { setRows } from '../../utils/set-rows';
import { messages } from '../../const';

const KnowledgesTable = (): JSX.Element => {
  const columnExtensions: Table.ColumnExtension[] = [
    { columnName: 'name', width: 230 },
    { columnName: 'body', width: 700 },
  ];

  const dispatch = useAppDispatch();
  const rows = useAppSelector(getRows);
  const columns = useAppSelector(getColumns);
  const isLoading = useAppSelector(getIsLoading);

  const [query, setQuery] = useState<string>('');
  const [selection, setSelection] = useState<(number | string)[]>([]);

  useEffect(() => {
    dispatch(fetchKnowledges());
  }, [dispatch]);

  return (
    <>
      <Navigation />
      <Toolbar onSearchChange={setQuery} />
      {
        isLoading ?
          <div className='spinner'>
            <Spinner animation='border' />
          </div>
          :
          <div className='table_container knowoledgesTable'>
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

export default KnowledgesTable;
