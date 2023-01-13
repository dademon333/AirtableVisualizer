import { Entity, State } from '../../types/types';

export const getIsLoading = (state: State): boolean => state.DATA.isLoading;

export const getIsRelatedEntitiesLoading = (state: State): boolean => state.DATA.isRelatedEntitiesLoading;

export const getIsAddDataModalOpen = (state: State): boolean => state.DATA.isAddDataModalOpen;

export const getRelatedEntities = (state: State): Entity[][] => state.DATA.relatedEntities;

export const getRelatedEntityTypeNames = (state: State): string[] => state.DATA.relatedEntityTypeNames;

export const getChosenEntitiesIDs = (state: State): number[] => {
  const chosenEntities = state.DATA.chosenEntities;
  const ids = chosenEntities.map((item) => item.entities.map((e) => e.value.id!));
  if (ids.length > 1) {
    const result: number[] = [];
    ids.forEach(e => e.forEach(a => result.push(a!)));
    return result;
  }
  return ids[0];
}
