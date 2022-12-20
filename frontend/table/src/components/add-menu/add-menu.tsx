import { useState } from 'react';
import { ActionCreatorWithPayload, AsyncThunk } from '@reduxjs/toolkit';
import { AxiosInstance } from 'axios';
import SearchIcon from '@mui/icons-material/Search';
import { State, AppDispatch, Row } from '../../types/types';
import { getSearchingElement } from '../../utils/get-searching-element';
import { useAppDispatch, useAppSelector } from '../../hooks';

type AddMenuProps = {
  names: string[];
  getConnectionNumber: (state: State) => number;
  changeConnectionNumber: ActionCreatorWithPayload<number>;
  fetchData: AsyncThunk<Row[], undefined, {
    dispatch: AppDispatch;
    state: State;
    extra: AxiosInstance
  }>;
}

export const AddMenu = ({ names, getConnectionNumber, changeConnectionNumber, fetchData }: AddMenuProps): JSX.Element => {
  const dispatch = useAppDispatch();
  
  const [isOpenAddMenu, setOpenAddMenu] = useState(false);
  const [query, setQuery] = useState<string>('');

  const connectionNumber = useAppSelector(getConnectionNumber);
  
  const initMenuNames = names.map((name) => { return {name, to: ''} });
  const menuNames = getSearchingElement({initData: initMenuNames, query});

  return (
    <div className="add_container">
      <span className={isOpenAddMenu ? "add opened" : "add"} onClick={ () => setOpenAddMenu(!isOpenAddMenu) } />
      { isOpenAddMenu &&
        <div className="addMenu">
          <div className="add_search">
            <SearchIcon />
            <input placeholder="Поиск" onChange={event => setQuery(event.target.value)} />
          </div>
          { menuNames.map((menuName, idx) => {
            return (
              <div 
                className={`addMenu_item ${connectionNumber === idx && 'checkMark'}`}
                key={`${idx}-${menuName}`}
                onClick={() => {
                  setOpenAddMenu(false);
                  dispatch(changeConnectionNumber(idx));
                  dispatch(fetchData());
                }}>
                  {menuName.name}
              </div>
            );
          }) }
        </div>
      }
    </div>
  );
};
