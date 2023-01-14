import { useState } from 'react';
import { OverlayTrigger, Popover } from 'react-bootstrap';
import ArrowRightAltOutlinedIcon from '@mui/icons-material/ArrowRightAltOutlined';
import SyncAltOutlinedIcon from '@mui/icons-material/SyncAltOutlined';
import AddCircleTwoToneIcon from '@mui/icons-material/AddCircleTwoTone';
import SearchIcon from '@mui/icons-material/Search';
import { ReactComponent as ToGraphIcon } from '../../assets/icons/to_graph.svg';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { SortingOptions, UserStatus } from '../../const';
import { AddDataWindow } from '../add-data-window/add-data-window';
import actions from '../../redux/change-data/change-data';
import { getAuthorizationStatus } from '../../redux/auth-actions/selectors';

type ToolbarProps = {
  onSearchChange: React.Dispatch<React.SetStateAction<string>>;
  sortingOption: SortingOptions;
  onSortingOption: React.Dispatch<React.SetStateAction<SortingOptions>>;
  queryLength: number;
};

const NoRightsPopover = (
  <Popover id="popover-basic" className='no-rights-popover'>
    <Popover.Header>
      У Вас нет прав, чтобы добавлять данные
    </Popover.Header>
  </Popover>
);

const Toolbar = ({onSearchChange, sortingOption, onSortingOption, queryLength}: ToolbarProps): JSX.Element => {
  const dispatch = useAppDispatch();
  const [isSortingOptionsOpen, setIsSortingOptionsOpen] = useState<boolean>(false);

  const authorizationStatus = useAppSelector(getAuthorizationStatus);

  return (
    <div className="toolbar">
      <div className="left">
        <div className={`search button ${queryLength !== 0 && 'active'}`}>
          <SearchIcon />
          <input
            placeholder="Поиск" 
            onChange={event => onSearchChange(event.target.value)}
          />
        </div>
        <div className={`sorting ${isSortingOptionsOpen && 'opened'} button`} 
          onClick={() => setIsSortingOptionsOpen(!isSortingOptionsOpen)}
        >
          <div className="sorting_text"><SyncAltOutlinedIcon /> Сортировка</div>
          <div className={isSortingOptionsOpen ? "options" : "options closed"}>
              <div className={`${sortingOption === SortingOptions.DEFAULT && 'option clicked'}`} onClick={() => onSortingOption(SortingOptions.DEFAULT)}>По дате</div>
              <div className={`${sortingOption === SortingOptions.ASC && 'option clicked'}`} onClick={() => onSortingOption(SortingOptions.ASC)}>
                А<ArrowRightAltOutlinedIcon fontSize='small' />Я
              </div>
              <div className={`${sortingOption === SortingOptions.DESC && 'option clicked'}`} onClick={() => onSortingOption(SortingOptions.DESC)}>
                Я<ArrowRightAltOutlinedIcon fontSize='small' />А
              </div>
          </div>
        </div>
        {
          authorizationStatus === UserStatus.Unauthorized
          ?
          <OverlayTrigger
            placement='bottom'
            overlay={NoRightsPopover}
            children={
              <div className="add-element button">
                <AddCircleTwoToneIcon /> Добавить данные
              </div>  
            }
          />
          :
          <div className="add-element button" onClick={() => dispatch(actions.changeAddDataModalOpen(true))}>
            <AddCircleTwoToneIcon /> Добавить данные
          </div>
        }
      </div>
      <div className="right">
        <div className="toGraph button">
          <a href='http://corevision.ru'>
            <ToGraphIcon />Перейти к графу
          </a>
        </div>
      </div>
      <AddDataWindow />
    </div> 
  );
}

export default Toolbar;