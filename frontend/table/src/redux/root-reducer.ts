import { combineReducers } from '@reduxjs/toolkit';
import { mainData } from './main-data/main-data';
import { usersData } from './users-page-data/users-page-data';

export const rootReducer = combineReducers({
  'DATA': mainData.reducer,
  'USERS': usersData.reducer,
});
