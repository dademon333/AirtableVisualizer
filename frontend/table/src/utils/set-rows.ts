import { Row } from "../types/types";

export const setRows = (rows: Row[], query: string): Row[] => {
  if (query !== '') {
    return rows
      .filter(row => {
        if (query === "") {
            return row;
        } else if (row.title.props.children.toLowerCase().trim().includes(query.toLowerCase().trim())) {
            return row;
        } else return null;
      })
  }
  return rows;
}