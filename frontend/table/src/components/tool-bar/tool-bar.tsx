import { useState } from 'react';
import { Link } from 'react-router-dom';
import ArrowRightAltOutlinedIcon from '@mui/icons-material/ArrowRightAltOutlined';
import SyncAltOutlinedIcon from '@mui/icons-material/SyncAltOutlined';
import SearchIcon from '@mui/icons-material/Search';
import { ReactComponent as ToGraphIcon } from '../../assets/icons/to_graph.svg';

type ToolbarProps = {
  onSearchChange: React.Dispatch<React.SetStateAction<string>>;
} 

const Toolbar = ({onSearchChange}: ToolbarProps) => {
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
              <div className={/* sortingOption === 'default' ? "option clicked":  */"default"} /* onClick={() => onSortingOptionClick('default')} */>По дате</div>
              <div className={/* sortingOption === 'asc' ? "option clicked":  */"asc"} /* onClick={() => onSortingOptionClick('asc')} */>
                  А<ArrowRightAltOutlinedIcon fontSize='small' />Я
              </div>
              <div className={/* sortingOption === 'desc' ? "option clicked":  */"desc"} /* onClick={() => onSortingOptionClick('desc')} */>
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