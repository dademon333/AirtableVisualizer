import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData } from '../../types/types';
import { Row, EntityConnection } from '../../types/types';
import { wrapSecondColElements, wrapFirstColElement } from '../../utils/wrap';
import { getChilds, getItems } from '../../utils/get-items';
import { getEmptyRow } from '../../utils/get-empty-Row';
import { APIRoute } from '../../const';
import { NameSpace } from '../../const';

export const fetchCourses = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.COURSES}/fetchData`,
  async (_arg, {dispatch, extra: api}) => {
    const courses = await api.get(`${APIRoute.Courses}${APIRoute.List}`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const connections: EntityConnection[] = data.entity_connections
      .filter((connection) => connection.type_connection_id === 16);
    const rows = courses.data.map((course: {id: number, name: string, description: string}) => {
      const row = getEmptyRow();
      const childs = getChilds(connections, course.id);
      const items = getItems([], childs, data);
      row.name = wrapFirstColElement(course.name);
      row.body = wrapSecondColElements(items);
      return row;
    });
    return rows;
  }
);