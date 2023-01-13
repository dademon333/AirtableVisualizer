import { useEffect, useState } from 'react';
import { PagingState, IntegratedPaging } from '@devexpress/dx-react-grid';
import { Grid, Table, TableHeaderRow } from '@devexpress/dx-react-grid-bootstrap4';
import { PagingPanel } from '@devexpress/dx-react-grid-material-ui';
import Spinner from 'react-bootstrap/Spinner';
import { useAppDispatch } from '../../hooks';
import { useAppSelector } from '../../hooks';
import { fetchThemes } from '../../redux/themes-data/api-actions';
import Navigation from '../../components/navigation/navigation';
import Toolbar from '../../components/tool-bar/tool-bar';
import { getRows, getColumns, getIsLoading } from '../../redux/themes-data/selectors';
import { setRows } from '../../utils/set-rows';
import { messages, SortingOptions } from '../../const';

const ThemesTable = (): JSX.Element => {
  const columnWidths: Table.ColumnExtension[] = [
    { columnName: 'id', width: 50 },
    { columnName: 'name', width: 230 },
    { columnName: 'body', width: 900 },
    { columnName: 'add', width: 65 }
  ];

  const dispatch = useAppDispatch();
  const rows = useAppSelector(getRows);
  const columns = useAppSelector(getColumns);
  const isLoading = useAppSelector(getIsLoading);

  const [query, setQuery] = useState<string>('');
  const [sortingOption, setSortingOption] = useState<SortingOptions>(SortingOptions.DEFAULT);

  useEffect(() => {
    dispatch(fetchThemes());
  }, [dispatch]);

  return (
    <>
      <Navigation />
      <Toolbar onSearchChange={setQuery} sortingOption={sortingOption} onSortingOption={setSortingOption} />
      {
        isLoading ?
          <div className='spinner'>
            <Spinner animation='border' />
          </div>
          :
          <div className='table_container themeTable'>
            <Grid
              rows={setRows(rows, query, sortingOption)}
              columns={columns}
            >
              <PagingState defaultCurrentPage={0} defaultPageSize={10} />
              <IntegratedPaging />
              <Table columnExtensions={columnWidths} />
              <PagingPanel pageSizes={[5, 10, 15, 0]} messages={messages} />
              <TableHeaderRow />
            </Grid>
          </div>
      }
    </>
    );
}

export default ThemesTable;
