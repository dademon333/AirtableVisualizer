import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, Entity } from '../../types/types';
import { APIRoute, NameSpace } from '../../const';

export const postEntity = createAsyncThunk<void, Entity, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.DATA}/postEntity`,
  async ({name, type, size, description, study_time}, {dispatch, extra: api, getState}) => {
    await api.post<Entity>(APIRoute.Entities, {
      name,
      type,
      size,
      description,
      study_time
    });
  }
);

export const deleteEntity = createAsyncThunk<void, number, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.DATA}/deleteEntity`,
  async (id, {dispatch, extra: api, getState}) => {
    await api.delete(`${APIRoute.Entities}/${id}`);
  }
);
