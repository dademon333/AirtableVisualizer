import React, { useState } from "react";
import { Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import TableLinks from "./TableLinks";
import './navigation.css';

const Navigation = ({ activeLink, Table }) => {
    const [isOpen, setOpen] = useState(false);

	return (
		<>
			<div className="finder-tables">
				<img className={`hamburger ${isOpen ? 'open' : 'closed'}`} src="icons/hamburger.svg" alt="hamburger" onClick={() => setOpen(!isOpen)} />
				{ isOpen ? <TableLinks setOpen={setOpen} /> : null }
			</div>
			<Nav variant="tabs">
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'course' ? 'active' : 'disable'}`} to="/">Курс</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'theme' ? 'active' : 'disable'}`} to="/theme">Тема</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'knowledge' ? 'active' : 'disable'}`} to="/knowledge">Знание</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'quantum' ? 'active' : 'disable'}`} to="/quantum">Кванты знаний</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'task' ? 'active' : 'disable'}`} to="/task">Задание</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'users' ? 'active' : 'disable'}`} to="/users">Пользователи</Link>
				</Nav.Item>
			</Nav>
			{Table}
		</>
	);
};

/* <>
		<img className="hamburger" src="icons/hamburger.svg" alt="hamburger" />
		<Tabs defaultActiveKey="course">
			<Tab eventKey="course" title="Курс">
				<CoursesTable />
			</Tab>
			<Tab eventKey="theme" title="Тема">
			</Tab>
			<Tab eventKey="knowledge" title="Знание">
			</Tab>
			<Tab eventKey="quantes" title="Кванты знаний">
			</Tab>
			<Tab eventKey="task" title="Задание">
			</Tab>
			<Tab eventKey="users" title="Пользователи">
			</Tab>
		</Tabs>
	</>
*/

export default Navigation;