import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PagingState, IntegratedPaging, SelectionState, IntegratedSelection } from '@devexpress/dx-react-grid';
import { Grid, Table, TableHeaderRow, TableSelection } from '@devexpress/dx-react-grid-bootstrap4';
import { PagingPanel } from '@devexpress/dx-react-grid-material-ui';
import Spinner from 'react-bootstrap/Spinner';
import { useAppSelector, useAppDispatch } from '../../hooks';
import Navigation from '../../components/navigation/navigation';
import Toolbar from '../../components/tool-bar/tool-bar';
import { getRows, getColumns, getIsLoading } from '../../redux/users-page-data/selectors';
import { getAuthorizationStatus } from '../../redux/auth-actions/selectors';
import { getUsersListAction } from '../../redux/users-page-data/api-actions';
import { messages, AppRoute, UserStatus } from '../../const';

const UsersTable = (): JSX.Element => {
  const columnExtensions: Table.ColumnExtension[] = [
    { columnName: 'id', width: '100px' },
    { columnName: 'name', width: '100px' },
    { columnName: 'email', width: '120px' },
    { columnName: 'status', width: '150px' },
    { columnName: 'created', width: '700px'}
  ];

  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const rows = useAppSelector(getRows);
  const columns = useAppSelector(getColumns);
  const isLoading = useAppSelector(getIsLoading);
  const authorizationStatus = useAppSelector(getAuthorizationStatus);

  const [query, setQuery] = useState<string>('');
  const [selection, setSelection] = useState<(number | string)[]>([]);

  useEffect(() => {
    if (authorizationStatus === UserStatus.Admin) {
      dispatch(getUsersListAction());
    } else {
      navigate(AppRoute.Main);
    }
  }, [authorizationStatus, dispatch, navigate]);

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
        <div className='table_container coursesTable'>
          <Grid
            rows={rows}
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
