import { useState } from 'react';
import { Link } from 'react-router-dom';
import ArrowRightAltOutlinedIcon from '@mui/icons-material/ArrowRightAltOutlined';
import SyncAltOutlinedIcon from '@mui/icons-material/SyncAltOutlined';
import SearchIcon from '@mui/icons-material/Search';
import { ReactComponent as ToGraphIcon } from '../../assets/icons/to_graph.svg';
import { SortingOptions } from '../../const';

type ToolbarProps = {
  onSearchChange: React.Dispatch<React.SetStateAction<string>>;
  sortingOption: SortingOptions;
  onSortingOption: React.Dispatch<React.SetStateAction<SortingOptions>>;
} 

const Toolbar = ({onSearchChange, sortingOption, onSortingOption}: ToolbarProps) => {
  const [isSortingOptionsOpen, setIsSortingOptionsOpen] = useState<boolean>(false);

  return (
    <div className="toolbar">
      <div className="left">
        <div className="search">
          <SearchIcon />
          <input 
              placeholder="Поиск" 
              onChange={event => onSearchChange(event.target.value)}
          />
        </div>
        <div className={`sorting ${isSortingOptionsOpen && 'opened'}`} 
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
      </div>
      <div className="right">
        <div className="toGraph">
          <Link to='#'>
            <ToGraphIcon />Перейти к графу
          </Link>
        </div>
      </div>
    </div> 
  );
}

export default Toolbar;