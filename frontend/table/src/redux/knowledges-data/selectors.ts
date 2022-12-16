import { State } from '../../types/types';
import { Column } from '@devexpress/dx-react-grid';
import { Row } from '../../types/types';

export const getRows = (state: State): Row[] => state.KNOWLEDGES.rows;

export const getColumns = (state: State): Column[] => state.KNOWLEDGES.columns;

export const getIsLoading = (state: State): boolean => state.KNOWLEDGES.isLoading;
