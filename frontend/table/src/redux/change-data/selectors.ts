import { State } from '../../types/types';

export const getIsLoading = (state: State): boolean => state.DATA.isLoading;

export const getIsAddDataModalOpen = (state: State): boolean => state.DATA.isAddDataModalOpen;
