import { createSlice } from '@reduxjs/toolkit';
import { Column } from '@devexpress/dx-react-grid';
import { fetchCourses } from '../courses-data/api-actions';
import { Row } from '../../types/types';
import { NameSpace } from '../../const';

const initialState: {
  rows: Row[];
  columns: Column[];
  isLoading: boolean;
} = {
  rows: [],
  columns: [
    { name: 'name', title: '' },
    { name: 'body', title: '' },
  ],
  isLoading: true,
};

export const coursesData = createSlice({
  name: NameSpace.COURSES,
  initialState,
  reducers: {
    changeNameColumn: (state, action) => {
      state.columns[0].title = action.payload;
    },
    changeBodyColumn: (state, action) => {
      state.columns[1].title = action.payload;
    }
  },
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

export default coursesData.actions;
