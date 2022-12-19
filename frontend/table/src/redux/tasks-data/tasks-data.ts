import { createSlice } from '@reduxjs/toolkit';
import { Column } from '@devexpress/dx-react-grid';
import { fetchTasks } from '../tasks-data/api-actions';
import { Row } from '../../types/types';
import { NameSpace } from '../../const';

const initialState: {
  rows: Row[];
  columns: Column[];
  isLoading: boolean;
} = {
  rows: [],
  columns: [
    { name: 'name', title: 'Задания' },
    { name: 'body', title: '' },
  ],
  isLoading: true,
};

export const tasksData = createSlice({
  name: NameSpace.TASKS,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder.addCase(fetchTasks.pending, (state) => {
      state.isLoading = true;
    })
    .addCase(fetchTasks.fulfilled, (state, action) => {
      state.rows = action.payload;
      state.isLoading = false;
    });
  }
});
