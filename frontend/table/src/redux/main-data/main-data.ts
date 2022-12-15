import { createSlice } from "@reduxjs/toolkit";
import { Column } from '@devexpress/dx-react-grid';
import { fetchData } from "../api-actions";
import { Row } from "../../types/types";

const initialState: {
  rows: Row[];
  columns: Column[];
  isLoading: boolean;
} = {
  rows: [],
  columns: [
    { name: 'title', title: 'Title' },
    { name: 'body', title: 'Body' },
  ],
  isLoading: true,
};

export const mainData = createSlice({
  name: 'DATA',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder.addCase(fetchData.pending, (state) => {
      state.isLoading = true;
    })
    .addCase(fetchData.fulfilled, (state, action) => {
      state.rows = action.payload;
      state.isLoading = false;
    });
  }
});
