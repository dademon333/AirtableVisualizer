import { createSlice } from '@reduxjs/toolkit';
import { Column } from '@devexpress/dx-react-grid';
import { fetchQuauntums } from '../quntams-data/api-actions';
import { Row } from '../../types/types';
import { NameSpace } from '../../const';

const initialState: {
  rows: Row[];
  columns: Column[];
  isLoading: boolean;
} = {
  rows: [],
  columns: [
    { name: 'name', title: 'Кванты' },
    { name: 'body', title: '' },
  ],
  isLoading: true,
};

export const quantumsData = createSlice({
  name: NameSpace.KNOWLEDGES,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder.addCase(fetchQuauntums.pending, (state) => {
      state.isLoading = true;
    })
    .addCase(fetchQuauntums.fulfilled, (state, action) => {
      state.rows = action.payload;
      state.isLoading = false;
    });
  }
});
