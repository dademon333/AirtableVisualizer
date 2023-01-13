import { Entity, State } from '../../types/types';

export const getIsLoading = (state: State): boolean => state.DATA.isLoading;

export const getIsRelatedEntitiesLoading = (state: State): boolean => state.DATA.isRelatedEntitiesLoading;

export const getIsAddDataModalOpen = (state: State): boolean => state.DATA.isAddDataModalOpen;

export const getRelatedEntities = (state: State): Entity[][] => state.DATA.relatedEntities;

export const getRelatedEntityTypeNames = (state: State): string[] => state.DATA.relatedEntityTypeNames;

export const getChosenEntities = (state: State): Entity[] => {
  const chosenEntities = state.DATA.chosenEntities;
  const entities = chosenEntities.map((item) => item.entities.map((e) => e.value));
  if (entities.length > 1) {
    const result: Entity[] = [];
    entities.forEach(entity => entity.forEach(e => result.push(e)));
    return result;
  }
  return entities[0];
};
