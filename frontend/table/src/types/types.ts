import { store } from '../redux/store';
import { EntityType, UserStatus } from '../const';

export type Row = {
  id: number;
  name: JSX.Element;
  body: JSX.Element;
  add?: JSX.Element;
};

export type UsersRow = {
  id: number;
  name: string;
  email: string;
  status: UserStatus;
  created: string;
};

export type EntityConnection = {
  child_id: number;
  id: number;
  parent_id: number;
  type_connection_id: number;
};

export type Course = {
  id: number;
  name: string;
  description: string;
};

export type Entity = {
  id?: number;
  name: string;
  type: string;
  size: string;
  description: string | null;
  study_time: number | null;
};

export type AllData = {
  courses: [];
  entities: Entity[];
  entity_connections: EntityConnection[];
};

export type TypeConnections = {
  id: number;
  parent_type: EntityType;
  child_type: EntityType;
  parent_column_name: string;
  child_column_name: string;
}

export type UserData = {
  access_token: string;
  token_type: string;
  detail: string;
  id: number,
  name: string,
  email: string,
  status: UserStatus,
  created_at: string;
}

export type AuthData = {
  email: string;
  password: string;
}

export type Response = {
  response: string;
  detail: string;
}

export type State = ReturnType<typeof store.getState>;

export type AppDispatch = typeof store.dispatch;