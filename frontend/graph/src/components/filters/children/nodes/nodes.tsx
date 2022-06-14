import { useSelector } from 'react-redux';
import { IFilterState, IVisibleEntity } from '../../../../redux/slices/filter.slice';
import './styles.css';
import { useEffect, useState } from 'react';
import { transformToElement } from '../../../../services/event.service';


export default function Nodes() {
    const [visibleEntities, setVisibleEntities] = useState<IVisibleEntity[]>([]);
    const data = useSelector((state: { filters: IFilterState }) => state.filters);
    const [input, setInput] = useState("");
    const [isVisible, setIsVisble] = useState<boolean>(false);
    useEffect(() => {
        const newVisibleEntities: IVisibleEntity[] = [];
        document.querySelectorAll('.node').forEach(el => {
            const opacity = el.getAttribute('opacity');
            if (opacity === '1') {
                const name = el.getAttribute('name')!;
                const id = el.getAttribute('id')!;
                if (!input || name.toLowerCase().includes(input.toLowerCase()))
                newVisibleEntities.push({name, id})

            }
        });

        setVisibleEntities(newVisibleEntities);
        setIsVisble(newVisibleEntities.length !== 0);
    }, [data, input])

    return (isVisible ? <div className="nodes">
        <h2 className="nodes-title">ВЕРШИНА</h2>
        <input className='nodes-search' type='text' onChange={(el) => setInput(el.target.value)}/>
        <div className='nodes-list-wrapper'>
        <ul className='nodes-list'>
            {visibleEntities.map(el => <li onClick={e => transformToElement(el.id)} className='nodes-list-item' key={el.id}>{el.name}</li>)}
        </ul>
        </div>

    </div> : <></>)
}

