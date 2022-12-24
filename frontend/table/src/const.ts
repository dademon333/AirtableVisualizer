import { ToastOptions } from 'react-toastify';

export const toastifyOptions: ToastOptions = {
  theme: 'colored',
  position: 'bottom-right',
  autoClose: 2500,
  toastId: 1,
};

export enum AppRoute {
  Main = '/table',
  Theme = '/table/theme',
  Knowledge = '/table/knowledge',
  Quantum = '/table/quantum',
  Target = '/table/target',
  Users = '/table/users'
};

export const messages = {showAll: 'Все', rowsPerPage: 'Строк на странице:'};

export enum APIRoute {
  Auth = '/auth',
  Users = '/users',
  Entities = '/entities',
  Courses = '/courses',
  TypeConnections = '/type_connections',
  EntityConnections = '/entity_connections',
  List = '/list',
  All = '/all',
  Search = '/search',
  Login = '/login',
  Logout = '/logout',
  Me = '/me',
};

export enum EntityType {
  EducationalProgram = 'educational program', 
  Course = 'course', 
  Theme = 'theme', 
  Knowledge = 'knowledge', 
  Quantum = 'quantum', 
  Target = 'target', 
  Metric = 'metric', 
  Task = 'task', 
  Activity = 'activity', 
  Skill = 'skill', 
  Competence = 'competence', 
  Profession = 'profession',
  SuosCompetence = 'suos_competence', 
  CompetenceModel = 'competence_model'
};

export enum NameSpace {
  COURSES = 'COURSES',
  THEMES = 'THEMES',
  KNOWLEDGES = 'KNOWLEDGES',
  QUANTUMS = 'QUANTUMS',
  TARGETS = 'TARGETS',
  AUTH = 'AUTH',
  USERS = 'USERS',
};

export enum UserStatus {
  User = 'user',
  Editor = 'editor',
  Admin = 'admin',
  Authorized = 'Authorized',
  Unauthorized = 'Unauthorized',
}
