import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import IEntitiesAndConnectionsResponse, { IConnection, IEntity } from '../../interfaces/response/entities-connections-response.interface';

const initialState : IEntitiesAndConnectionsResponse = {
    connections: [],
    entities: {},
    visibleEntities: {}
};
export interface IVisibleEntity {
  nodes: object[],
  links: object[]
}

export const entityConnectionSlice = createSlice({
  name: 'course',
  initialState,
  reducers: {
    setConnectionsAndEntities: (state, action: PayloadAction<IEntitiesAndConnectionsResponse>) => {
      state.connections = action.payload.connections;
      state.entities = action.payload.entities;
    },
    setConnections: (state, action: PayloadAction<IConnection[]>) => {
        state.connections = action.payload;
    },
    setEntities: (state, action: PayloadAction<{ [id: string]: IEntity }>) => {
        state.entities = action.payload;
    },
    setVisibleEntites: (state, action: PayloadAction<IVisibleEntity[]>) => {
      state.visibleEntities = action.payload;
   },
    
  },
});

export const { setConnectionsAndEntities, setConnections, setEntities, setVisibleEntites } = entityConnectionSlice.actions;

export default entityConnectionSlice.reducer;