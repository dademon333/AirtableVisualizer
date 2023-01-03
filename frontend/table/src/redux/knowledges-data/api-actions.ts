import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData, Entity } from '../../types/types';
import { Row, TypeConnections } from '../../types/types';
import { APIRoute, NameSpace, EntityType } from '../../const';
import actions from './knowledges-data';
import { getAddMenu } from '../../pages/knowledges-table/get-add-menu';
import { dispatchActions } from '../../utils/dispatch-actions';
import { makeRows } from '../../utils/make-rows';

export const fetchKnowledges = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.KNOWLEDGES}/fetchData`,
  async (_arg, {dispatch, extra: api, getState}) => {
    const knowledges = await api.get<Entity[]>(`${APIRoute.Entities}${APIRoute.List}/${EntityType.Knowledge}?limit=1000`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const typeConnections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
    
    const connectionNumber = getState().KNOWLEDGES.connectionNumber;
    const types = typeConnections.data
      .filter(e => (e.parent_type === EntityType.Knowledge || e.child_type === EntityType.Knowledge) && e.child_column_name !== null);

    dispatchActions({
      connectionNumber,
      entityType: EntityType.Knowledge,
      dispatch,
      types,
      actions: {
        changeNameColumn: actions.changeNameColumn,
        changeBodyColumn: actions.changeBodyColumn,
        changeAddColumn: actions.changeAddColumn
      },
      getAddMenu
    });

    return makeRows({items: knowledges.data, connectionNumber, data, entityType: EntityType.Knowledge, types});
  }
);