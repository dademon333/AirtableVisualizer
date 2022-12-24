import { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CoursesTable, ThemesTable, KnowledgesTable, QuantumsTable, TargetsTable, UsersTable } from './pages';
import { Login } from './components/login/login';
import { AppRoute, UserStatus } from './const';
import { getAuthorizationStatus } from './redux/auth-actions/selectors';
import { useAppDispatch, useAppSelector } from './hooks';
import { getMeAction } from './redux/auth-actions/auth-actions';

function App() {
  const dispatch = useAppDispatch();
  const authorizationStatus = useAppSelector(getAuthorizationStatus);

  useEffect(() => {
    if (authorizationStatus === UserStatus.Authorized || authorizationStatus === UserStatus.Unauthorized) {
      dispatch(getMeAction());
    }
  }, [authorizationStatus, dispatch]);

  return (
    <BrowserRouter>
      <Login />
      <div className="App">
        <Routes>
            <Route path={AppRoute.Main} element={ <CoursesTable /> } />
            <Route path={AppRoute.Theme} element={ <ThemesTable /> } />
            <Route path={AppRoute.Knowledge} element={ <KnowledgesTable /> } />
            <Route path={AppRoute.Quantum} element={ <QuantumsTable /> } />
            <Route path={AppRoute.Target} element={ <TargetsTable /> } />
            <Route path={AppRoute.Users} element={ <UsersTable /> } />
          </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
