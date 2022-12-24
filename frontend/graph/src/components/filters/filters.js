import { ReactComponent as NodeType } from '../../assets/nodeType.svg';
import { ReactComponent as LookingGlass } from '../../assets/lookingGlass.svg';
import './style.css';
import { useState } from 'react';
import NodeTypeSearch from './children/nodeType/NodeTypeSearch';
import { useDispatch } from 'react-redux';
import { setComponentType } from '../../redux/slices/filter.slice';

export default function Filters() {

    const dispatch = useDispatch()

    const [isSelected, setIsSelected] = useState('none')

    const onClickArrow = () => {
        setIsSelected('none')
        dispatch(dispatch(setComponentType([])))
    }

    if (isSelected === 'none')
    {return (
    <div className="filters">
        <h2 className="filters-title">ФИЛЬТРЫ</h2>
        <div className="select-button" onClick={() => setIsSelected('nodeType')}>
            <NodeType className="select-button-icon"/>
            <span className="select-button-title"> Типы вершин</span>
        </div>

        <div className="select-button">
            <LookingGlass className="select-button-icon"/>
            <span className="select-button-title"> Поиск вершин по названию</span>
        </div>
    </div>
    )}
    else if (isSelected == 'nodeType')
    {return (
        <NodeTypeSearch onClickArrow={onClickArrow}/>
    )}
}

//<ShortestPath />