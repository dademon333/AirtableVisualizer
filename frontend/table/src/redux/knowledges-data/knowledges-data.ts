import { createSlice } from '@reduxjs/toolkit';
import { Column } from '@devexpress/dx-react-grid';
import { fetchKnowledges } from '../knowledges-data/api-actions';
import { Row } from '../../types/types';
import { NameSpace } from '../../const';

const initialState: {
  rows: Row[];
  columns: Column[];
  isLoading: boolean;
} = {
  rows: [],
  columns: [
    { name: 'name', title: 'Знания' },
    { name: 'body', title: 'Компетенции' },
  ],
  isLoading: true,
};

export const knowledgesData = createSlice({
  name: NameSpace.KNOWLEDGES,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder.addCase(fetchKnowledges.pending, (state) => {
      state.isLoading = true;
    })
    .addCase(fetchKnowledges.fulfilled, (state, action) => {
      state.rows = action.payload;
      state.isLoading = false;
    });
  }
});
