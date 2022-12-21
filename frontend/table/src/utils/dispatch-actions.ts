import { ActionCreatorWithPayload, Dispatch } from '@reduxjs/toolkit';
import { EntityType } from '../const';
import { TypeConnections } from '../types/types';

type DispatchActionsProps = {
  connectionNumber: number; 
  entityType: EntityType;
  types: TypeConnections[];
  dispatch: Dispatch;
  actions: {
    changeNameColumn: ActionCreatorWithPayload<string>,
    changeBodyColumn: ActionCreatorWithPayload<string>,
    changeAddColumn: ActionCreatorWithPayload<JSX.Element>
  };
  getAddMenu: (connections: TypeConnections[], type: EntityType) => JSX.Element;
}

export const dispatchActions = ({ connectionNumber, entityType, types, dispatch, actions, getAddMenu }: DispatchActionsProps) => {
  dispatch(actions.changeNameColumn(types[connectionNumber].parent_type === entityType ?
    types[connectionNumber].parent_column_name
    : types[connectionNumber].child_column_name));
  dispatch(actions.changeBodyColumn(types[connectionNumber].child_type !== entityType ?
    types[connectionNumber].child_column_name
    : types[connectionNumber].parent_column_name));
  dispatch(actions.changeAddColumn(getAddMenu(types, entityType)));
};