import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData, Entitiy } from '../../types/types';
import { Row, EntityConnection, TypeConnections } from '../../types/types';
import { wrapSecondColElements, wrapFirstColElement } from '../../utils/wrap';
import { getChilds, getItems } from '../../utils/get-items';
import { getEmptyRow } from '../../utils/get-empty-Row';
import { APIRoute, NameSpace, EntityType } from '../../const';

export const fetchTasks = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.TASKS}/fetchData`,
  async (_arg, {dispatch, extra: api}) => {
    const tasks = await api.get<Entitiy[]>(`${APIRoute.Entities}${APIRoute.List}/${EntityType.Task}?limit=1000`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const typeConnections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
    
    const type = typeConnections.data.filter(e => (e.parent_type === EntityType.Task || e.child_type === EntityType.Task) && e.child_column_name !== null)[0];
    console.log(type);
    const connections: EntityConnection[] = data.entity_connections
      .filter((connection) => connection.type_connection_id === type.id);
    const rows = tasks.data.map((task) => {
      const row = getEmptyRow();
      const childs = getChilds(connections, task.id);
      const items = getItems([], childs, data);
      row.name = wrapFirstColElement(task.name);
      row.body = wrapSecondColElements(items);
      return row;
    });
    return rows;
  }
);