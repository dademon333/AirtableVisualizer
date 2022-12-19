import { State } from '../../types/types';
import { Column } from '@devexpress/dx-react-grid';
import { Row } from '../../types/types';

export const getRows = (state: State): Row[] => state.TASKS.rows;

export const getColumns = (state: State): Column[] => state.TASKS.columns;

export const getIsLoading = (state: State): boolean => state.TASKS.isLoading;
