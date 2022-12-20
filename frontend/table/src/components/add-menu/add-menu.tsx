import { useState } from 'react';
import SearchIcon from '@mui/icons-material/Search';
import { TypeConnections } from '../../types/types';
import { getSearchingElement } from '../../utils/get-searching-element';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { getConnectionNumber } from '../../redux/targets-data/selectors';
import { fetchTargets } from '../../redux/targets-data/api-actions';
import actions from '../../redux/targets-data/targets-data';

type AddMenuProps = {
  names: string[];
}

const AddMenu = ({ names }: AddMenuProps): JSX.Element => {
  const dispatch = useAppDispatch();
  
  const [isOpenAddMenu, setOpenAddMenu] = useState(false);
  const [query, setQuery] = useState<string>('');
  const activeItem = useAppSelector(getConnectionNumber);
  
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
                className={`addMenu_item ${activeItem === idx && 'checkMark'}`}
                key={`${idx}-${menuName}`}
                onClick={() => {
                  setOpenAddMenu(false);
                  dispatch(actions.changeConnectionNumber(idx));
                  dispatch(fetchTargets());
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

export const getAddMenu = (props: TypeConnections[]) => {
  const names = props.map((p) => p.child_column_name);

  return <AddMenu names={names} />;
};