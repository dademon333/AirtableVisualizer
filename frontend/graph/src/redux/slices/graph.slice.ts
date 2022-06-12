import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import INode from '../../interfaces/graph/node.interface';
import ILink from '../../interfaces/graph/nodes-link.interface';

export interface IGraphState {
  nodes: INode[],
  links: ILink[]
}

const initialState: IGraphState = {
  nodes:[],
  links: []
};

export const graphSlice = createSlice({
  name: 'graph',
  initialState,
  reducers: {
    setNodes: (state, action: PayloadAction<INode[]>) => {
      state.nodes = action.payload;
    },
    setLinks: (state, action: PayloadAction<ILink[]>) => {
        state.links = action.payload;
    }
  },
});

export const { setNodes, setLinks } = graphSlice.actions;

export default graphSlice.reducer;