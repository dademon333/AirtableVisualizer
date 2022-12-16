import { store } from '../redux/store';

export type Row = {
  id: number;
  name: JSX.Element;
  body: JSX.Element;
};

export type EntityConnection = {
  child_id: number,
  id: number,
  parent_id: number,
  type_connection_id: number
}

export type AllData = {
  courses: [],
  entities: {
    id: number,
    name: string,
    type: string,
    size: string,
    description: null,
    study_time: null
  }[],
  entity_connections: EntityConnection[]
}

export type State = ReturnType<typeof store.getState>;

export type AppDispatch = typeof store.dispatch;