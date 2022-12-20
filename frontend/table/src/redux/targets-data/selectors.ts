import { State } from '../../types/types';
import { Column } from '@devexpress/dx-react-grid';
import { Row } from '../../types/types';

export const getRows = (state: State): Row[] => state.TARGETS.rows;

export const getColumns = (state: State): Column[] => state.TARGETS.columns;

export const getIsLoading = (state: State): boolean => state.TARGETS.isLoading;

export const getConnectionNumber = (state: State): number => state.TARGETS.connectionNumber;
