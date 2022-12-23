import { createAsyncThunk } from "@reduxjs/toolkit";
import { AxiosInstance } from "axios";
import { State, AppDispatch, UserData } from "../../types/types";
import { APIRoute, NameSpace } from "../../const";

type AuthData = {
  email: string;
  password: string;
}

type Detail = {
  detail: string;
}

type Response = {
  response: string;
}

export const loginAction = createAsyncThunk<UserData, AuthData, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.AUTH}/login`,
  async ({email, password}, {dispatch, extra: api}) => {
    const {data} = await api.post<UserData>(`${APIRoute.Auth}/login`, {email, password});
    return data;
  }
);

export const logoutAction = createAsyncThunk<void, undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.AUTH}/logout`,
  async (_arg, {dispatch, extra: api}) => {
    const {data} = await api.delete<Response | Detail>(`${APIRoute.Auth}/logout`);
    console.log(data);
  }
);