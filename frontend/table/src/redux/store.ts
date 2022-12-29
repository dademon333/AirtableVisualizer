import { configureStore } from '@reduxjs/toolkit';
import axios, { AxiosInstance, AxiosError, AxiosRequestConfig } from 'axios';
import { toast } from 'react-toastify';
import { toastifyOptions, UserStatus } from '../const';
import { rootReducer } from './root-reducer';
import { getUser } from '../services/user';

const BASE_URL = 'http://corevision.ru/api';
const REQUEST_TIMEOUT = 10000;

const createAPI = (): AxiosInstance => {
  const api = axios.create({
    baseURL: BASE_URL,
    timeout: REQUEST_TIMEOUT,
    withCredentials: true
  });

  api.interceptors.request.use((config: AxiosRequestConfig) => {
    const user = getUser();

    if (user && config.headers) {
      config.headers['Authorization'] = `Bearer ${user.access_token}`;
    }

    return config;
  });
  
  api.interceptors.response.use(
    (response) => response,
    (error: AxiosError<{ detail: string }>) => {
      if (error.response) {
        if (error.response.data.detail !== UserStatus.Unauthorized) {
          toast.error(error.response.data.detail, toastifyOptions);
        }
      }

      throw error;
    }
  );

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
