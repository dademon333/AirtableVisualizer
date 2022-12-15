import { State } from '../../types/types';
import { Column } from '@devexpress/dx-react-grid';
import { Row } from '../../types/types';

export const getRows = (state: State): Row[] => state.DATA.rows;

export const getColumns = (state: State): Column[] => state.DATA.columns;

export const getIsLoading = (state: State): boolean => state.DATA.isLoading;
