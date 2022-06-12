import { useSelector } from 'react-redux';
import { IFilterState } from '../../../../redux/slices/filter.slice';
import './styles.css';

export default function Nodes() {
    
    const visibleEntities = useSelector((state: { filters: IFilterState }) => {
        return state.filters.components.visibleEntities;
    });

    return (<div className="nodes">
        <h2 className="nodes-title">ВЕРШИНА</h2>
        <input className='nodes-search' type='text'/>
        <ul className='nodes-list'>
            {visibleEntities.map(el => <li>{el.name}</li>)}
        </ul>
    </div>)
}
