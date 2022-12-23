import { createSlice } from '@reduxjs/toolkit';
import { loginAction } from './auth-actions';
import { UserStatus, NameSpace } from '../../const';

const initialState: {
  authorizationStatus: UserStatus;
} = {
  authorizationStatus: UserStatus.Unauthorized,
};

export const authProcess = createSlice({
  name: NameSpace.AUTH,
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addCase(loginAction.fulfilled, (state, action) => {
        state.authorizationStatus = UserStatus.User;
        console.log(state.authorizationStatus);
        console.log(action.payload);
      })
      .addCase(loginAction.rejected, (state) => {
        state.authorizationStatus = UserStatus.Unauthorized;
      });
  }
})