import React, { useState } from "react";
import { Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import TableLinks from "./TableLinks";
import './navigation.css';
import { ReactComponent as SearchTableIcon} from '../../icons/hamburger.svg';


const Navigation = ({ activeLink, Table }) => {
    const [isOpen, setOpen] = useState(false);

	return (
		<>
			<div className="finder-tables">
				<div className={`hamburger ${isOpen ? 'open' : 'closed'}`} onClick={() => setOpen(!isOpen)}>
					<SearchTableIcon />
				</div>
				{ isOpen ? <TableLinks setOpen={setOpen} /> : null }
			</div>
			<Nav variant="tabs">
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'course' ? 'active' : 'disable'}`} to="/table/">Курс</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'theme' ? 'active' : 'disable'}`} to="/table/theme">Тема</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'knowledge' ? 'active' : 'disable'}`} to="/table/knowledge">Знание</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'quantum' ? 'active' : 'disable'}`} to="/table/quantum">Кванты знаний</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'task' ? 'active' : 'disable'}`} to="/table/task">Задание</Link>
				</Nav.Item>
				<Nav.Item>
					<Link className={`nav-link ${activeLink === 'users' ? 'active' : 'disable'}`} to="/table/users">Пользователи</Link>
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