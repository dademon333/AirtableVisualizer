import { createSlice } from '@reduxjs/toolkit';
import { Column } from '@devexpress/dx-react-grid';
import { fetchCourses } from '../courses-data/api-actions';
import { Row } from '../../types/types';

const initialState: {
  rows: Row[];
  columns: Column[];
  isLoading: boolean;
} = {
  rows: [],
  columns: [
    { name: 'name', title: 'Курс' },
    { name: 'body', title: 'Темы' },
  ],
  isLoading: true,
};

export const coursesData = createSlice({
  name: 'DATA',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder.addCase(fetchCourses.pending, (state) => {
      state.isLoading = true;
    })
    .addCase(fetchCourses.fulfilled, (state, action) => {
      state.rows = action.payload;
      state.isLoading = false;
    });
  }
});
