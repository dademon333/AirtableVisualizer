import React from "react";
import Navigation from "./components/Navigation/Navigation";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CoursesTable, ThemesTable, KnowledgesTable, QuantsTable, TasksTable } from './components/Tables';

function App() {
  return (
      <BrowserRouter>
        <div className="App">
          <div className="core">
            <p>Ядро N курсов</p>
            <div className="arrow"><img src="icons/arrow.svg" alt="arrow" /></div>
          </div>
          <div className="account">
            <img src="icons/account.svg" alt="account" />
          </div>
          <Routes>
            <Route path="/" element={ <Navigation activeLink="course" Table={ <CoursesTable /> } /> } />
            <Route path="/theme" element={ <Navigation activeLink="theme" Table={ <ThemesTable /> } /> } />
            <Route path="/knowledge" element={ <Navigation activeLink="knowledge" Table={ <KnowledgesTable /> } /> } />
            <Route path="/quantum" element={ <Navigation activeLink="quantum" Table={ <QuantsTable /> } /> } />
            <Route path="/task" element={ <Navigation activeLink="task" Table={ <TasksTable /> } /> } />
            <Route path="/users" element={ <Navigation activeLink="users" /> } />
          </Routes>
        </div>
      </BrowserRouter>
  );
}

export default App;
