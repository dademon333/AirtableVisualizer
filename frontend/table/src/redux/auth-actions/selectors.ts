import { State } from '../../types/types';

export const getAuthorizationStatus = (state: State) => state.AUTH.authorizationStatus;

export const getUserEmail = (state: State) => state.AUTH.userEmail;

export const getIsLoading = (state: State) => state.AUTH.isLoading;

export const getIsOpen = (state: State) => state.AUTH.isOpen;
