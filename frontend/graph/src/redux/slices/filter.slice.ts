import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import EntityType from '../../enums/entity-type.enum';
import SetType from '../../enums/set-type.enum';

export interface IFilterState {
  components: {
    /** Тип сущности */
    types: Array<EntityType>,

    /** id сущностей */
    entities: Array<string>,

    /** Тип множества */
    setType: SetType,

    /** id всех сущностей, которые видны */
    visibleEntities: Array<IVisibleEntity>
  }
}

export interface IVisibleEntity {
  nodes: object[],
  links: object[]
}

const initialState: IFilterState = {
  components: {
    types: [],
    entities: [],
    setType: SetType.Union,
    visibleEntities: []
  }
};

export const filterSlice = createSlice({
  name: 'filter',
  initialState,
  reducers: {
    setComponentType: (state, action: PayloadAction<EntityType[]>) => {
        state.components.types = action.payload;
    },
    addComponentEntity: (state, action: PayloadAction<string>) => {
        state.components.entities = [...state.components.entities, action.payload];
    },
    removeComponentEntity: (state, action: PayloadAction<string>) => {
      state.components.entities = state.components.entities.filter(entity => entity !== action.payload);
    },
    setComponentSetType: (state, action: PayloadAction<SetType>) => {
        state.components.setType = action.payload;
    },
    setComponentEntities: (state, action: PayloadAction<string[]>) => {
      state.components.entities = action.payload;
    },
    setSetType: (state, action: PayloadAction<SetType>) => {
       state.components.setType = action.payload;
    },
    setVisibleEntites: (state, action: PayloadAction<IVisibleEntity[]>) => {
      state.components.visibleEntities = action.payload;
   },
  },
});

export const { setComponentType, addComponentEntity, removeComponentEntity, setComponentSetType, setComponentEntities, setSetType, setVisibleEntites } = filterSlice.actions;

export default filterSlice.reducer;