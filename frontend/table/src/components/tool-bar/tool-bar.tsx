import { useState } from 'react';
import { Link } from 'react-router-dom';
import ArrowRightAltOutlinedIcon from '@mui/icons-material/ArrowRightAltOutlined';
import SyncAltOutlinedIcon from '@mui/icons-material/SyncAltOutlined';
import AddCircleTwoToneIcon from '@mui/icons-material/AddCircleTwoTone';
import SearchIcon from '@mui/icons-material/Search';
import { ReactComponent as ToGraphIcon } from '../../assets/icons/to_graph.svg';
import { EntityType, SortingOptions } from '../../const';
import { AddDataWindow } from '../add-data-window/add-data-window';

type ToolbarProps = {
  onSearchChange: React.Dispatch<React.SetStateAction<string>>;
  sortingOption: SortingOptions;
  onSortingOption: React.Dispatch<React.SetStateAction<SortingOptions>>;
  entityType: EntityType;
} 

const Toolbar = ({onSearchChange, sortingOption, onSortingOption, entityType}: ToolbarProps): JSX.Element => {
  const [isSortingOptionsOpen, setIsSortingOptionsOpen] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(false);

  return (
    <div className="toolbar">
      <div className="left">
        <div className="search button">
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
        <div className="add-element button" onClick={() => setShowModal(true)}>
          <AddCircleTwoToneIcon /> Добавить данные
        </div>
      </div>
      <div className="right">
        <div className="toGraph button">
          <Link to='#'>
            <ToGraphIcon />Перейти к графу
          </Link>
        </div>
      </div>
      <AddDataWindow showModal={showModal} onHide={setShowModal} entityType={entityType} />
    </div> 
  );
}

export default Toolbar;