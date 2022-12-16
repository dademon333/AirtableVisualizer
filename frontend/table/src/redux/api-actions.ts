import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State } from '../types/types';
import { APIRoute } from '../const';

export const fetchData = createAsyncThunk<null, undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  'DATA/fetchData',
  async (_arg, {dispatch, extra: api}) => {
    const {data} = await api.get(`${APIRoute.Courses}${APIRoute.List}`);
    return data;
  }
);
