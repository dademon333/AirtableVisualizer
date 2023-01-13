import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, Entity, TypeConnections } from '../../types/types';
import { APIRoute, NameSpace, EntityType } from '../../const';
import { fetchCourses } from '../courses-data/api-actions';
import { fetchThemes } from '../themes-data/api-actions';
import { fetchKnowledges } from '../knowledges-data/api-actions';
import { fetchQuauntums } from '../quntums-data/api-actions';
import { fetchTargets } from '../targets-data/api-actions';
import { filterTypeConnections } from '../../utils/get-type-connections';

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

type RelatedEntityType = {
  type: EntityType,
  name: string
};

type RelatedEntity = {
  data: Entity[],
  name: string
};

export const fetchRelatedEntityTypes = createAsyncThunk<void, EntityType, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.DATA}/fetchRelatedEntityTypes`,
  async (entityType, {dispatch, extra: api, getState}) => {
    const {data} = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
    const typeConnections = filterTypeConnections({entityType, typeConnections: data});

    const entityTypes: RelatedEntityType[] = typeConnections.map((connection) => {
      if (connection.parent_type === entityType) {
        return {
          type: connection.child_type,
          name: connection.child_column_name
        };
      } else {
        return {
          type: connection.parent_type,
          name: connection.parent_column_name
        };
      }
    });

    entityTypes.forEach((type) => {
      dispatch(fetchRelatedEntities(type));
    });
  }
);

export const fetchRelatedEntities = createAsyncThunk<RelatedEntity, {type: EntityType, name: string}, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.DATA}/fetchRelatedEntities`,
  async ({type, name}, {dispatch, extra: api, getState}) => {
    const {data} = await api.get<Entity[]>(`${APIRoute.Entities}${APIRoute.List}/${type}?limit=1000`);
    return {
      data,
      name
    };
  }
);
