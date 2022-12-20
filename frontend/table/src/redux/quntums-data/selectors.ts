import { State } from '../../types/types';
import { Column } from '@devexpress/dx-react-grid';
import { Row } from '../../types/types';

export const getRows = (state: State): Row[] => state.QUANTUMS.rows;

export const getColumns = (state: State): Column[] => state.QUANTUMS.columns;

export const getIsLoading = (state: State): boolean => state.QUANTUMS.isLoading;

export const getConnectionNumber = (state: State): number => state.QUANTUMS.connectionNumber;
