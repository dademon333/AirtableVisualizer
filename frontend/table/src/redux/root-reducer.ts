import { combineReducers } from '@reduxjs/toolkit';
import { coursesData } from './courses-data/courses-data';
import { themesData } from './themes-data/themes-data';
import { usersData } from './users-page-data/users-page-data';
import { knowledgesData } from './knowledges-data/knowledges-data';
import { quantumsData } from './quntams-data/quantums-data';
import { tasksData } from './tasks-data/tasks-data';
import { NameSpace } from '../const';

export const rootReducer = combineReducers({
  [NameSpace.COURSES]: coursesData.reducer,
  [NameSpace.THEMES]: themesData.reducer,
  [NameSpace.KNOWLEDGES]: knowledgesData.reducer,
  [NameSpace.QUANTUMS]: quantumsData.reducer,
  [NameSpace.TASKS]: tasksData.reducer,
  [NameSpace.USERS]: usersData.reducer,
});
