import { createSlice } from '@reduxjs/toolkit';
import { Column } from '@devexpress/dx-react-grid';
import { fetchThemes } from '../themes-data/api-actions';
import { Row } from '../../types/types';
import { NameSpace } from '../../const';

const initialState: {
  rows: Row[];
  columns: Column[];
  isLoading: boolean;
} = {
  rows: [],
  columns: [
    { name: 'name', title: 'Тема' },
    { name: 'body', title: 'Знания' },
  ],
  isLoading: true,
};

export const themesData = createSlice({
  name: NameSpace.THEMES,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder.addCase(fetchThemes.pending, (state) => {
      state.isLoading = true;
    })
    .addCase(fetchThemes.fulfilled, (state, action) => {
      state.rows = action.payload;
      state.isLoading = false;
    });
  }
});
