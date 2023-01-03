import { Row } from '../types/types';
import { comparePriority } from './compare-priority';
import { SortingOptions } from '../const';

export const setRows = (rows: Row[], query: string, sortingOption: SortingOptions): Row[] => {
  const sortedData = 
    sortingOption === SortingOptions.DEFAULT ? rows :
    sortingOption === SortingOptions.ASC ? rows.slice().sort((row1, row2) => comparePriority(row1.name.props.entity.name, row2.name.props.entity.name)) :
    sortingOption === SortingOptions.DESC ? rows.slice().sort((row1, row2) => comparePriority(row2.name.props.entity.name, row1.name.props.entity.name))
    : null;
  
  if (query !== '' && sortedData) {
    return sortedData
      .filter(row => {
        if (query === "") {
            return row;
        } else if (row.name.props.entity.name.toLowerCase().trim().includes(query.toLowerCase().trim())) {
            return row;
        } else return null;
      });
  }
  return sortedData!;
}