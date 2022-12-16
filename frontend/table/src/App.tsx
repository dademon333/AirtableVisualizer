import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CoursesTable, ThemesTable, KnowledgesTable, QuantumsTable, TasksTable, UsersTable } from './pages';
import { AppRoute } from './const';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
            <Route path={AppRoute.Main} element={ <CoursesTable /> } />
            <Route path={AppRoute.Theme} element={ <ThemesTable /> } />
            <Route path={AppRoute.Knowledge} element={ <KnowledgesTable /> } />
            {/* <Route path={AppRoute.Quantum} element={ <QuantumsTable /> } />
            <Route path={AppRoute.Task} element={ <TasksTable /> } />
            <Route path={AppRoute.Users} element={ <UsersTable /> } /> */}
          </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
