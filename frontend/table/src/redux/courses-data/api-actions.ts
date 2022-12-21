import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData, Course } from '../../types/types';
import { Row, EntityConnection, TypeConnections } from '../../types/types';
import { APIRoute, NameSpace, EntityType } from '../../const';
import actions from './courses-data';
import { getAddMenu } from '../../pages/courses-table/get-add-menu';
import { dispatchActions } from '../../utils/dispatch-actions';
import { makeRows } from '../../utils/make-rows';

export const fetchCourses = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.COURSES}/fetchData`,
  async (_arg, {dispatch, extra: api, getState}) => {
    const courses = await api.get<Course[]>(`${APIRoute.Courses}${APIRoute.List}`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const typeConnections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
    
    const connectionNumber = getState().COURSES.connectionNumber;
    const types = typeConnections
      .data.filter(e => (e.parent_type === EntityType.Course || e.child_type === EntityType.Course) && e.child_column_name !== null);
    
    dispatchActions({
      connectionNumber,
      entityType: EntityType.Course,
      dispatch,
      types,
      actions: {
        changeNameColumn: actions.changeNameColumn,
        changeBodyColumn: actions.changeBodyColumn,
        changeAddColumn: actions.changeAddColumn
      },
      getAddMenu
    });

    const connections: EntityConnection[] = data.entity_connections
      .filter((connection) => connection.type_connection_id === types[connectionNumber].id);

    return makeRows({items: courses.data, connections, data, entityType: EntityType.Course, typeConnection: types[connectionNumber]});
  }
);