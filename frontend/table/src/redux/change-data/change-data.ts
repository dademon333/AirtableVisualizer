import { createSlice } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';
import { NameSpace, toastifyOptions } from '../../const';
import { postEntity, deleteEntity } from './api-actions';

const initialState: {
  isLoading: boolean;
} = {
  isLoading: false,
};

export const coursesData = createSlice({
  name: NameSpace.DATA,
  initialState,
  reducers:{},
  extraReducers(builder) {
    builder
      .addCase(postEntity.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(postEntity.rejected, (state) => {
        state.isLoading = false;
        toast.warning('Не удалось добавить данные', toastifyOptions);
      })
      .addCase(postEntity.fulfilled, (state) => {
        state.isLoading = false;
        toast.success('Данные добавлены!', toastifyOptions);
      });
  }
});
