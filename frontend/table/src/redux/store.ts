import { configureStore } from '@reduxjs/toolkit';
import axios, { AxiosInstance }from 'axios';
import { rootReducer } from './root-reducer';

const BASE_URL = 'http://corevision.ru/api';
const REQUEST_TIMEOUT = 10000;

const createAPI = (): AxiosInstance => {
  const api = axios.create({
    baseURL: BASE_URL,
    timeout: REQUEST_TIMEOUT,
  });
  return api;
}

const api = createAPI();

export const store = configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) => 
        getDefaultMiddleware({
            serializableCheck: false, 
            thunk: {
                extraArgument: api
            },
        })
});
