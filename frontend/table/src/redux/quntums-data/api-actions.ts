import { AxiosInstance } from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { AppDispatch, State, AllData, Entity } from '../../types/types';
import { Row, TypeConnections } from '../../types/types';
import { APIRoute, NameSpace, EntityType } from '../../const';
import actions from './quantums-data';
import { getAddMenu } from '../../pages/quantums-table/get-add-menu';
import { dispatchActions } from '../../utils/dispatch-actions';
import { makeRows } from '../../utils/make-rows';

export const fetchQuauntums = createAsyncThunk<Row[], undefined, {
  dispatch: AppDispatch,
  state: State,
  extra: AxiosInstance
}
>(
  `${NameSpace.QUANTUMS}/fetchData`,
  async (_arg, {dispatch, extra: api, getState}) => {
    const quantums = await api.get<Entity[]>(`${APIRoute.Entities}${APIRoute.List}/${EntityType.Quantum}?limit=1000`);
    const {data} = await api.get<AllData>(`${APIRoute.Courses}${APIRoute.All}`);
    const typeConnections = await api.get<TypeConnections[]>(`${APIRoute.TypeConnections}${APIRoute.List}`);
    
    const connectionNumber = getState().QUANTUMS.connectionNumber;
    const types = typeConnections.data
      .filter(e => (e.parent_type === EntityType.Quantum || e.child_type === EntityType.Quantum) && e.child_column_name !== null);
    
    dispatchActions({
      connectionNumber,
      entityType: EntityType.Quantum,
      dispatch,
      types,
      actions: {
        changeNameColumn: actions.changeNameColumn,
        changeBodyColumn: actions.changeBodyColumn,
        changeAddColumn: actions.changeAddColumn
      },
      getAddMenu
    });

    return makeRows({items: quantums.data, connectionNumber, data, entityType: EntityType.Quantum, types});
  }
);
