import { State } from '../../types/types';
import { Column } from '@devexpress/dx-react-grid';
import { UsersRow } from '../../types/types';

export const getRows = (state: State): UsersRow[] => state.USERS.rows;

export const getColumns = (state: State): Column[] => state.USERS.columns;

export const getIsLoading = (state: State): boolean => state.USERS.isLoading;
