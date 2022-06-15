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
            <Route path="/routes/" element={ <Navigation activeLink="course" Table={ <CoursesTable /> } /> } />
            <Route path="/routes/theme" element={ <Navigation activeLink="theme" Table={ <ThemesTable /> } /> } />
            <Route path="/routes/knowledge" element={ <Navigation activeLink="knowledge" Table={ <KnowledgesTable /> } /> } />
            <Route path="/routes/quantum" element={ <Navigation activeLink="quantum" Table={ <QuantsTable /> } /> } />
            <Route path="/routes/task" element={ <Navigation activeLink="task" Table={ <TasksTable /> } /> } />
            <Route path="/routes/users" element={ <Navigation activeLink="users" /> } />
          </Routes>
        </div>
      </BrowserRouter>
  );
}

export default App;
