import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import EntityType from '../../enums/entity-type.enum';
import SetType from '../../enums/set-type.enum';

export interface IFilterState {
  components: {
    type?: EntityType,
    entities: Array<EntityType>,
    setType: SetType
  }
}

const initialState: IFilterState = {
  components: {
    type: undefined,
    entities: [],
    setType: SetType.Union
  }
};

export const filterSlice = createSlice({
  name: 'filter',
  initialState,
  reducers: {
    setComponentType: (state, action: PayloadAction<EntityType>) => {
      state.components.type = action.payload;
    },
    addComponentEntity: (state, action: PayloadAction<EntityType>) => {
        state.components.entities = [...state.components.entities, action.payload];
    },
    removeComponentEntity: (state, action: PayloadAction<EntityType>) => {
      state.components.entities = state.components.entities.filter(entity => entity !== action.payload);
    },
    setComponentSetType: (state, action: PayloadAction<SetType>) => {
        state.components.setType = action.payload;
    }
  },
});

export const { setComponentType, addComponentEntity, removeComponentEntity, setComponentSetType } = filterSlice.actions;

export default filterSlice.reducer;