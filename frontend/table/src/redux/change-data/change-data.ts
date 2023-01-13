import { createSlice } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';
import { NameSpace, toastifyOptions } from '../../const';
import { Entity, SelectConnectWithOption } from '../../types/types';
import { postEntity, deleteEntity, fetchRelatedEntityTypes, fetchRelatedEntities } from './api-actions';

type ChosenEntity = {
  name: string;
  entities: SelectConnectWithOption[];
}

const initialState: {
  isLoading: boolean;
  isRelatedEntitiesLoading: boolean;
  isAddDataModalOpen: boolean;
  relatedEntities: Entity[][];
  relatedEntityTypeNames: string[];
  chosenEntities: ChosenEntity[];
} = {
  isLoading: false,
  isRelatedEntitiesLoading: false,
  isAddDataModalOpen: false,
  relatedEntities: [],
  relatedEntityTypeNames: [],
  chosenEntities: [],
};

export const changeData = createSlice({
  name: NameSpace.DATA,
  initialState,
  reducers:{
    changeAddDataModalOpen: (state, action) => {
      state.isAddDataModalOpen = action.payload;
    },
    clearRelatedEntities: (state) => {
      state.relatedEntities = [];
      state.relatedEntityTypeNames = [];
      state.chosenEntities = [];
    },
    updateChosenEntities: (state, action: {type: string; payload: ChosenEntity}) => {
      const currentChosenEntityType = state.chosenEntities.filter((e) => e.name === action.payload.name)[0];
      if (!currentChosenEntityType) {
        state.chosenEntities.push({
          name: action.payload.name,
          entities: action.payload.entities
        });
      } else {
        const chosenType = state.chosenEntities.filter((e) => e.name === currentChosenEntityType.name)[0];
        const index = state.chosenEntities.indexOf(chosenType);
        state.chosenEntities.splice(index, 1);
        
        if (action.payload.entities.length !== 0) {
          state.chosenEntities.push(action.payload);
        }
      }
    }
  },
  extraReducers(builder) {
    builder
      .addCase(postEntity.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(postEntity.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAddDataModalOpen = false;
        state.relatedEntities = [];
        state.relatedEntityTypeNames = [];
        state.chosenEntities = [];
        toast.success('Данные добавлены!', toastifyOptions);
      })
      .addCase(postEntity.rejected, (state) => {
        state.isLoading = false;
        state.isAddDataModalOpen = true;
        toast.warning('Не удалось добавить данные', toastifyOptions);
      })
      .addCase(deleteEntity.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(deleteEntity.fulfilled, (state) => {
        state.isLoading = false;
        toast.success('Данные успешно удалены!', toastifyOptions);
      })
      .addCase(deleteEntity.rejected, (state) => {
        state.isLoading = false;
        toast.warning('Не удалось удалить данные', toastifyOptions);
      })
      .addCase(fetchRelatedEntityTypes.pending, (state) => {
        state.isRelatedEntitiesLoading = true;
      })
      .addCase(fetchRelatedEntityTypes.fulfilled, (state, action) => {
        state.relatedEntities = [];
        state.relatedEntityTypeNames = [];
      })
      .addCase(fetchRelatedEntities.pending, (state) => {
        state.isRelatedEntitiesLoading = true;
      })
      .addCase(fetchRelatedEntities.fulfilled, (state, action) => {
        state.isRelatedEntitiesLoading = false;
        state.relatedEntities.push(action.payload.data);
        state.relatedEntityTypeNames.push(action.payload.name);
      });
  }
});

export default changeData.actions;
