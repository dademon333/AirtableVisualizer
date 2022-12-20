import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData, Entitiy } from '../../types/types';
import { Row, EntityConnection, TypeConnections } from '../../types/types';
import { wrapSecondColElements, wrapFirstColElement } from '../../utils/wrap';
import { getChilds, getItems } from '../../utils/get-items';
import { getEmptyRow } from '../../utils/get-empty-Row';
import { APIRoute, NameSpace, EntityType } from '../../const';
import actions from './knowledges-data';
import { getAddMenu } from '../../pages/knowledges-table/get-add-menu';

export const fetchKnowledges = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.KNOWLEDGES}/fetchData`,
  async (_arg, {dispatch, extra: api, getState}) => {
    const knowledges = await api.get<Entitiy[]>(`${APIRoute.Entities}${APIRoute.List}/${EntityType.Knowledge}?limit=1000`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const typeConnections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
    
    const connectionNumber = getState().KNOWLEDGES.connectionNumber;
    const types = typeConnections.data.filter(e => e.parent_type === EntityType.Knowledge && e.child_column_name !== null);

    dispatch(actions.changeNameColumn(types[connectionNumber].parent_column_name));
    dispatch(actions.changeBodyColumn(types[connectionNumber].child_column_name));
    dispatch(actions.changeAddColumn(getAddMenu(types)));

    const connections: EntityConnection[] = data.entity_connections
      .filter((connection) => connection.type_connection_id === types[connectionNumber].id);
    
      const rows = knowledges.data.map((knowledge) => {
      const row = getEmptyRow();
      const childs = getChilds(connections, knowledge.id);
      const items = getItems([], childs, data);
      row.name = wrapFirstColElement(knowledge.name);
      row.body = wrapSecondColElements(items);
      return row;
    });
    return rows;
  }
);