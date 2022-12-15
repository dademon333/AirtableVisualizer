import { store } from '../redux/store';

export type Row = {
  id: string;
  title: JSX.Element;
  body: JSX.Element;
};


export type State = ReturnType<typeof store.getState>;

export type AppDispatch = typeof store.dispatch;