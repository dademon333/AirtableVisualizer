import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import ISelect from '../../../../interfaces/control/select.interface';
import SelectModel from '../../../../models/select/select.model';
import { IFilterState } from '../../../../redux/slices/filter.slice';
import { getVisibleNodes } from '../../../../services/graph.service';
import Select from '../../../select/select';
import './styles.css';
import { ReactComponent as Plus } from '../../../../assets/plus.svg';
import { ReactComponent as Minus } from '../../../../assets/minus.svg';



interface IEdge {
    from: SelectModel<string>,
    //type: SeleсtModel<>,
    to: SelectModel<string>
}


export default function Links() {
    //const [visibleNodes, setVisibleNodes] = useState<IVisibleEntity[]>([]);
    const [edges, setEdges] = useState<IEdge[]>([]);
    const [isVisible, setIsVisible] = useState<boolean>(false);

    const data = useSelector((state: { filters: IFilterState }) => state.filters);

    useEffect(() => {
        const visibleNodes = getVisibleNodes();
        const shouldBeVisible = visibleNodes.length !== 0;
        setIsVisible(shouldBeVisible);

        const items: ISelect<string>[] = visibleNodes.map(node => {
            const item: ISelect<string> = {
                id: node.id,
                name: node.name
            };

            return item;
        });

        const model1 = new SelectModel(items);
        const model2 = new SelectModel(items);
        setEdges([{from: model1, to: model2}]);
    }, [data]);



    return isVisible ? 
    <div className="links">
        <h2 className="links-title">РЁБРА</h2>
        {edges.map(edge => {
            return (<div>
                <Select model={edge.from} />
                <Select model={edge.to} />
            </div>)
        })}
        <div className='links-actions'>
            <Plus />
            <Minus />
        </div>
    </div> : <></>
}

