import { Row } from "../types/types";

export const wrapFirstColElement = (rows: Row[]) => {
  const rowsCopy = rows;
  return rowsCopy.map(row => (
    row.title = <div className="first-column-element">{row.title}</div>
  ));
};

export const wrapSecColElement = (rows: Row[]) => {
  const rowsCopy = rows;
  return rowsCopy.map(row => (
    row.body = 
    <div className='secondary-column-elements'>
      <div className="secondary-column-element">{row.title}</div>
      <div className="secondary-column-element">{row.title}</div>
      <div className="secondary-column-element">{row.title}</div>
    </div>
  ));
};
