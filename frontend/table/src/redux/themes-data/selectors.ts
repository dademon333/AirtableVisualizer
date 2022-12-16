import { State } from '../../types/types';
import { Column } from '@devexpress/dx-react-grid';
import { Row } from '../../types/types';

export const getRows = (state: State): Row[] => state.THEMES.rows;

export const getColumns = (state: State): Column[] => state.THEMES.columns;

export const getIsLoading = (state: State): boolean => state.THEMES.isLoading;
