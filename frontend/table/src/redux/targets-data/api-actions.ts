import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData, Entity } from '../../types/types';
import { Row, TypeConnections } from '../../types/types';
import { APIRoute, NameSpace, EntityType } from '../../const';
import actions from './targets-data';
import { getAddMenu } from '../../pages/targets-table/get-add-menu';
import { dispatchActions } from '../../utils/dispatch-actions';
import { makeRows } from '../../utils/make-rows';

export const fetchTargets = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.TARGETS}/fetchData`,
  async (_arg, {dispatch, extra: api, getState}) => {
    const targets = await api.get<Entity[]>(`${APIRoute.Entities}${APIRoute.List}/${EntityType.Target}?limit=1000`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const typeConnections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);

    const connectionNumber = getState().TARGETS.connectionNumber;
    const types = typeConnections.data
      .filter(e => (e.parent_type === EntityType.Target || e.child_type === EntityType.Target) && e.child_column_name !== null);

    dispatchActions({
      connectionNumber,
      entityType: EntityType.Target,
      dispatch,
      types,
      actions: {
        changeNameColumn: actions.changeNameColumn,
        changeBodyColumn: actions.changeBodyColumn,
        changeAddColumn: actions.changeAddColumn
      },
      getAddMenu
    });
    
    return makeRows({items: targets.data, connectionNumber, data, entityType: EntityType.Target, types});
  }
);