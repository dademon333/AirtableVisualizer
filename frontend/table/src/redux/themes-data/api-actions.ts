import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData, Entitiy } from '../../types/types';
import { Row, EntityConnection, TypeConnections } from '../../types/types';
import { wrapSecondColElements, wrapFirstColElement } from '../../utils/wrap';
import { getChilds, getItems } from '../../utils/get-items';
import { getEmptyRow } from '../../utils/get-empty-Row';
import { APIRoute, NameSpace, EntityType } from '../../const';
import actions from './themes-data';

export const fetchThemes = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.THEMES}/fetchData`,
  async (_arg, {dispatch, extra: api}) => {
    const themes = await api.get<Entitiy[]>(`${APIRoute.Entities}${APIRoute.List}/${EntityType.Theme}?limit=1000`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const typeConnections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
    
    const type = typeConnections.data.filter(e => e.parent_type === EntityType.Theme && e.child_column_name !== null)[0];
    dispatch(actions.changeNameColumn(type.parent_column_name));
    dispatch(actions.changeBodyColumn(type.child_column_name));

    const connections: EntityConnection[] = data.entity_connections
      .filter((connection) => connection.type_connection_id === type.id);

    const rows = themes.data.map((theme) => {
      const row = getEmptyRow();
      const childs = getChilds(connections, theme.id);
      const items = getItems([], childs, data);
      row.name = wrapFirstColElement(theme.name);
      row.body = wrapSecondColElements(items);
      return row;
    });
    return rows;
  }
);