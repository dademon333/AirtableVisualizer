import { createSlice } from '@reduxjs/toolkit';
import { Column } from '@devexpress/dx-react-grid';
import { fetchCourses } from '../courses-data/api-actions';
import { Row } from '../../types/types';
import { NameSpace } from '../../const';

const initialState: {
  rows: Row[];
  columns: Column[];
  isLoading: boolean;
  connectionNumber: number;
} = {
  rows: [],
  columns: [
    { name: 'id', title: ' ' },
    { name: 'name', title: '' },
    { name: 'body', title: '' },
    { name: 'add', title: '' }
  ],
  isLoading: true,
  connectionNumber: 0,
};

export const coursesData = createSlice({
  name: NameSpace.COURSES,
  initialState,
  reducers: {
    changeNameColumn: (state, action) => {
      state.columns[1].title = action.payload;
    },
    changeBodyColumn: (state, action) => {
      state.columns[2].title = action.payload;
    },
    changeAddColumn: (state, action) => {
      state.columns[3].title = action.payload;
    },
    changeConnectionNumber: (state, action) => {
      state.connectionNumber = action.payload;
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
