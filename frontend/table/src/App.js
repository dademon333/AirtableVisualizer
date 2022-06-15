import React from "react";
import Navigation from "./components/Navigation/Navigation";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CoursesTable, ThemesTable, KnowledgesTable, QuantsTable, TasksTable } from './components/Tables';
import { ReactComponent as ArrowIcon } from './icons/arrow.svg';
import { ReactComponent as AccountIcon } from './icons/account.svg';

function App() {
  return (
      <BrowserRouter>
        <div className="App">
          <div className="core">
            <p>Ядро N курсов</p>
            <div className="arrow"><ArrowIcon /></div>
          </div>
          <div className="account">
            <AccountIcon />
          </div>
          <Routes>
            <Route path="/table/" element={ <Navigation activeLink="course" Table={ <CoursesTable /> } /> } />
            <Route path="/table/theme" element={ <Navigation activeLink="theme" Table={ <ThemesTable /> } /> } />
            <Route path="/table/knowledge" element={ <Navigation activeLink="knowledge" Table={ <KnowledgesTable /> } /> } />
            <Route path="/table/quantum" element={ <Navigation activeLink="quantum" Table={ <QuantsTable /> } /> } />
            <Route path="/table/task" element={ <Navigation activeLink="task" Table={ <TasksTable /> } /> } />
            <Route path="/table/users" element={ <Navigation activeLink="users" /> } />
          </Routes>
        </div>
      </BrowserRouter>
  );
}

export default App;
