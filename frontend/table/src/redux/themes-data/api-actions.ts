import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData, Entity } from '../../types/types';
import { Row, EntityConnection, TypeConnections } from '../../types/types';
import { APIRoute, NameSpace, EntityType } from '../../const';
import actions from './themes-data';
import { getAddMenu } from '../../pages/themes-table/get-add-menu';
import { dispatchActions } from '../../utils/dispatch-actions';
import { makeRows } from '../../utils/make-rows';

export const fetchThemes = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.THEMES}/fetchData`,
  async (_arg, {dispatch, extra: api, getState}) => {
    const themes = await api.get<Entity[]>(`${APIRoute.Entities}${APIRoute.List}/${EntityType.Theme}?limit=1000`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const typeConnections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
    
    const connectionNumber = getState().THEMES.connectionNumber;
    const types = typeConnections.data
      .filter(e => (e.parent_type === EntityType.Theme || e.child_type === EntityType.Theme) && e.child_column_name !== null);

    dispatchActions({
      connectionNumber,
      entityType: EntityType.Theme,
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

    return makeRows({items: themes.data, connections, data, entityType: EntityType.Theme, typeConnection: types[connectionNumber]});
  }
);