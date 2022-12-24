import { createSlice } from '@reduxjs/toolkit';
import { Column } from '@devexpress/dx-react-grid';
import { UsersRow } from "../../types/types";
import { getUsersListAction } from './api-actions';

const initialState: {
  rows: UsersRow[];
  columns: Column[];
  isLoading: boolean;
} = {
  rows: [],
  columns: [
    { name: 'id', title: 'Id' },
    { name: 'name', title: 'Имя' },
    { name: 'email', title: 'Email' },
    { name: 'status', title: 'Статус' },
    { name: 'created', title: 'Время создания' },
  ],
  isLoading: true,
};

export const usersData = createSlice({
  name: 'USERS',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addCase(getUsersListAction.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getUsersListAction.fulfilled, (state, action) => {
        state.rows = action.payload;
        state.isLoading = false;
      })
  }
});
