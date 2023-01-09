import { createSlice } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';
import { loginAction, logoutAction, getMeAction } from './auth-actions';
import { UserStatus, NameSpace, toastifyOptions } from '../../const';
import { saveUser, removeUser } from '../../services/user';

const initialState: {
  authorizationStatus: UserStatus;
  userEmail: string;
  isLoading: boolean;
  isOpen: boolean;
} = {
  authorizationStatus: UserStatus.Unauthorized,
  userEmail: '',
  isLoading: false,
  isOpen: false,
};

export const authProcess = createSlice({
  name: NameSpace.AUTH,
  initialState,
  reducers: {
    changeIsOpen: (state, action) => {
      state.isOpen = action.payload;
    }
  },
  extraReducers(builder) {
    builder
    .addCase(loginAction.pending, (state) => {
      state.isLoading = true;
    })
      .addCase(loginAction.fulfilled, (state, action) => {
        state.authorizationStatus = UserStatus.Authorized;
        state.isLoading = false;
        state.isOpen = false;
        saveUser(action.payload);
      })
      .addCase(loginAction.rejected, (state) => {
        state.authorizationStatus = UserStatus.Unauthorized;
        state.isLoading = false;
      })
      .addCase(getMeAction.fulfilled, (state, action) => {
        state.authorizationStatus = action.payload.status;
        state.userEmail = action.payload.email;
        toast.success(`Добро пожаловать, ${action.payload.name}!`, toastifyOptions);
      })
      .addCase(logoutAction.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(logoutAction.fulfilled, (state, action) => {
        removeUser();
        state.authorizationStatus = UserStatus.Unauthorized;
        state.userEmail = '';
        state.isLoading = false;
        state.isOpen = false;
        toast.warning('Вы вышли из системы!', toastifyOptions);
      });
  }
});

export default authProcess.actions;
