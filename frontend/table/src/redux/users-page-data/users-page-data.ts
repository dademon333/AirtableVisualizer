import { createSlice } from "@reduxjs/toolkit";
import { Column } from '@devexpress/dx-react-grid';
import { Row } from "../../types/types";

const initialState: {
  rows: Row[];
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
});
