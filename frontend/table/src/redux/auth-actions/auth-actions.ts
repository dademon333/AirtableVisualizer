import { createAsyncThunk } from "@reduxjs/toolkit";
import { AxiosInstance } from "axios";
import { State, AppDispatch, UserData, AuthData, Response } from "../../types/types";
import { APIRoute, NameSpace } from "../../const";

export const loginAction = createAsyncThunk<UserData, AuthData, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.AUTH}/login`,
  async ({email, password}, {dispatch, extra: api}) => {
    const {data} = await api.post<UserData>(`${APIRoute.Auth}${APIRoute.Login}`, {email, password});
    return data;
  }
);

export const logoutAction = createAsyncThunk<Response, undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.AUTH}/logout`,
  async (_arg, {dispatch, extra: api}) => {
    const {data} = await api.delete<Response>(`${APIRoute.Auth}${APIRoute.Logout}`);
    return data;
  }
);

export const getMeAction = createAsyncThunk<UserData, undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.AUTH}/getMe`,
  async (_arg, {dispatch, extra: api}) => {
    const {data} = await api.get<UserData>(`${APIRoute.Users}${APIRoute.Me}`);
    return data;
  }
);
