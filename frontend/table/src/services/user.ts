import { UserData } from '../types/types';

const KEY_NAME = 'user-data';

export const getUser = (): UserData | null => {
  const user = localStorage.getItem(KEY_NAME);
  return user ? JSON.parse(user) : null;
};

export const saveUser = (user: UserData): void => {
  localStorage.setItem(KEY_NAME, JSON.stringify(user));
};

export const removeUser = (): void => {
  localStorage.removeItem(KEY_NAME);
};
