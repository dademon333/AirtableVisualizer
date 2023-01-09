import { createSlice } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';
import { NameSpace, toastifyOptions } from '../../const';
import { postEntity, deleteEntity } from './api-actions';

const initialState: {
  isLoading: boolean;
  isAddDataModalOpen: boolean;
} = {
  isLoading: false,
  isAddDataModalOpen: false,
};

export const changeData = createSlice({
  name: NameSpace.DATA,
  initialState,
  reducers:{
    changeAddDataModalOpen: (state, action) => {
      state.isAddDataModalOpen = action.payload;
    }
  },
  extraReducers(builder) {
    builder
      .addCase(postEntity.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(postEntity.fulfilled, (state) => {
        state.isLoading = false;
        state.isAddDataModalOpen = false;
        toast.success('Данные добавлены!', toastifyOptions);
      })
      .addCase(postEntity.rejected, (state) => {
        state.isLoading = false;
        state.isAddDataModalOpen = true;
        toast.warning('Не удалось добавить данные', toastifyOptions);
      })
      .addCase(deleteEntity.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(deleteEntity.fulfilled, (state) => {
        state.isLoading = false;
        toast.success('Данные успешно удалены!', toastifyOptions);
      })
      .addCase(deleteEntity.rejected, (state) => {
        state.isLoading = false;
        toast.warning('Не удалось удалить данные', toastifyOptions);
      });
  }
});

export default changeData.actions;
