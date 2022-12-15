import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State } from '../types/types';
import { Row } from '../types/types';
import { wrapSecColElement, wrapFirstColElement } from '../utils/wrap';

export const fetchData = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  'DATA/fetchData',
  async (_arg, {dispatch, extra: api}) => {
    const {data} = await api.get<Row[]>('/posts');
    wrapSecColElement(data);
    wrapFirstColElement(data);
    return data;
  }
);

export const postElement = createAsyncThunk<void, object, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  'DATA/addElement', 
  async (_arg, {dispatch, extra: api}) => {
    const {data} = await api.post('/posts', _arg);
    console.log(data);
});
