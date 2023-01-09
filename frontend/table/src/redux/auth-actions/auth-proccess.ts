import { createSlice } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';
import { loginAction, logoutAction, getMeAction } from './auth-actions';
import { UserStatus, NameSpace, toastifyOptions } from '../../const';
import { saveUser, removeUser } from '../../services/user';

const initialState: {
  authorizationStatus: UserStatus;
  userEmail: string;
} = {
  authorizationStatus: UserStatus.Unauthorized,
  userEmail: '',
};

export const authProcess = createSlice({
  name: NameSpace.AUTH,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addCase(loginAction.fulfilled, (state, action) => {
        state.authorizationStatus = UserStatus.Authorized;
        saveUser(action.payload);
      })
      .addCase(loginAction.rejected, (state) => {
        state.authorizationStatus = UserStatus.Unauthorized;
      })
      .addCase(getMeAction.fulfilled, (state, action) => {
        state.authorizationStatus = action.payload.status;
        state.userEmail = action.payload.email;
        toast.success(`Добро пожаловать, ${action.payload.name}!`, toastifyOptions);
      })
      .addCase(logoutAction.fulfilled, (state, action) => {
        removeUser();
        state.authorizationStatus = UserStatus.Unauthorized;
        state.userEmail = '';
        toast.warning('Вы вышли из системы!', toastifyOptions);
      });
  }
})