import { combineReducers } from '@reduxjs/toolkit';
import { coursesData } from './courses-data/courses-data';
import { usersData } from './users-page-data/users-page-data';
import { NameSpace } from '../const';

export const rootReducer = combineReducers({
  [NameSpace.COURSES]: coursesData.reducer,
  [NameSpace.USERS]: usersData.reducer,
});
