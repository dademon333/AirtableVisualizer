import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, Entity } from '../../types/types';
import { APIRoute, NameSpace, EntityType } from '../../const';
import { fetchCourses } from '../courses-data/api-actions';
import { fetchThemes } from '../themes-data/api-actions';
import { fetchKnowledges } from '../knowledges-data/api-actions';
import { fetchQuauntums } from '../quntums-data/api-actions';
import { fetchTargets } from '../targets-data/api-actions';

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

    switch (type) {
      case EntityType.Course:
        await dispatch(fetchCourses());
        break;
      case EntityType.Theme:
        await dispatch(fetchThemes());
        break;
      case EntityType.Knowledge:
        await dispatch(fetchKnowledges());
        break;
      case EntityType.Quantum:
        await dispatch(fetchQuauntums());
        break;
      case EntityType.Target:
        await dispatch(fetchTargets());
        break;
    }
  }
);

export const deleteEntity = createAsyncThunk<void, {id: number, entityType: EntityType | string}, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.DATA}/deleteEntity`,
  async ({id, entityType}, {dispatch, extra: api, getState}) => {
    await api.delete(`${APIRoute.Entities}/${id}`);

    switch (entityType) {
      case EntityType.Course:
        await dispatch(fetchCourses());
        break;
      case EntityType.Theme:
        await dispatch(fetchThemes());
        break;
      case EntityType.Knowledge:
        await dispatch(fetchKnowledges());
        break;
      case EntityType.Quantum:
        await dispatch(fetchQuauntums());
        break;
      case EntityType.Target:
        await dispatch(fetchTargets());
        break;
    }
  }
);

export const getEntity = createAsyncThunk<Entity, number, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.DATA}/getEntity`,
  async (id, {dispatch, extra: api, getState}) => {
    const {data} = await api.get(`${APIRoute.Entities}/${id}`);
    return data;
  }
);
