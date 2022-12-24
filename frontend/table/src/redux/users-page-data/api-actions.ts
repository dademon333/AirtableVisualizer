import { createAsyncThunk } from '@reduxjs/toolkit';
import { AxiosInstance } from 'axios';
import { State, AppDispatch, UserData, UsersRow} from '../../types/types';
import { APIRoute, NameSpace, UserStatus } from '../../const';

export const getUsersListAction = createAsyncThunk<UsersRow[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.USERS}/getUsersList`,
  async (_arg, {dispatch, extra: api}) => {
    const {data} = await api.get<UserData[]>(`${APIRoute.Users}${APIRoute.List}`);

    return data.map((row): UsersRow => ({
      id: row.id,
      name: row.name,
      email: row.email,
      status: row.status,
      created: new Date(row.created_at).toLocaleString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
      })
    }));
  }
);