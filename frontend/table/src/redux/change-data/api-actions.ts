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

export const postEntity = createAsyncThunk<void, {entity: Entity, relatedEntities?: Entity[]}, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.DATA}/postEntity`,
  async ({entity, relatedEntities}, {dispatch, extra: api, getState}) => {
    const {name, type, size, description, study_time} = entity;
    const {data} = await api.post<Entity>(APIRoute.Entities, {
      name,
      type,
      size,
      description,
      study_time
    });

    if (relatedEntities) {
      const connections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
      const typeConnections = filterTypeConnections({entityType: type!, typeConnections: connections.data});
      relatedEntities.forEach((entity) => {
        const filteredType = typeConnections.filter((connection) => connection.child_type === entity.type || connection.parent_type === entity.type)[0];
        if (filteredType.parent_type === type) {
          dispatch(postEntityConnections({
            parent_id: data.id!,
            child_id: entity.id!
          }));
        } else {
          dispatch(postEntityConnections({
            parent_id: entity.id!,
            child_id: data.id!
          }));
        }
      });
    };

    switch (type) {
      case EntityType.Course:
        dispatch(fetchCourses());
        break;
      case EntityType.Theme:
        dispatch(fetchThemes());
        break;
      case EntityType.Knowledge:
        dispatch(fetchKnowledges());
        break;
      case EntityType.Quantum:
        dispatch(fetchQuauntums());
        break;
      case EntityType.Target:
        dispatch(fetchTargets());
        break;
    };
  }
);

export const postEntityConnections = createAsyncThunk<void, {parent_id: number, child_id: number}, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.DATA}/postEntityConnections`,
  async ({parent_id, child_id}, {dispatch, extra: api, getState}) => {
    await api.post<Entity>(APIRoute.EntityConnections, {parent_id, child_id});
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
        dispatch(fetchCourses());
        break;
      case EntityType.Theme:
        dispatch(fetchThemes());
        break;
      case EntityType.Knowledge:
        dispatch(fetchKnowledges());
        break;
      case EntityType.Quantum:
        dispatch(fetchQuauntums());
        break;
      case EntityType.Target:
        dispatch(fetchTargets());
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
