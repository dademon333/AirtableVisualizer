import { useEffect, useState } from 'react';
import ISelect from '../../../../interfaces/control/select.interface';
import SelectModel from '../../../../models/select/select.model';
import { onVisibleNodesChange } from '../../../../services/event.service';
import { getShortestPath } from '../../../../services/graph.service';
import Select from '../../../select/select';
import './styles.css';


export default function ShortestPath() {
    const [isVisible, setIsVisible] = useState<boolean>(false);
    const [modelFrom, setModelFrom] = useState<SelectModel<string>>(new SelectModel([]));
    const [modelTo, setModelTo] = useState<SelectModel<string>>(new SelectModel([]));

    useEffect(() => {
        onVisibleNodesChange().subscribe(visibleNodes => {
            const items = visibleNodes.map(ent => {
                const item: ISelect<string> = {
                    id: ent.id,
                    name: ent.name
                };
    
                return item;
            });

            setIsVisible(items.length !== 0);
            setModelFrom(new SelectModel(items, {}, modelFrom.SelectedItem || undefined));
            setModelTo(new SelectModel(items,{}, modelTo.SelectedItem || undefined));
        });


    // eslint-disable-next-line
    }, []);

    useEffect(() => {
        console.log('here');
        modelFrom.OnItemChange.subscribe((item) => {
            if (item && modelTo.SelectedItem) {
                console.log(getShortestPath(item.id, modelTo.SelectedItem.id));
            }
        });

        modelTo.OnItemChange.subscribe((item) => {
            if (item && modelFrom.SelectedItem) {
                console.log(getShortestPath(item.id, modelFrom.SelectedItem.id));
            }
        });
    }, [modelFrom, modelTo]);

    return isVisible ? <div className="shortest-path">
        <h2 className="shortest-path-title">КРАТЧАЙШИЙ ПУТЬ</h2>
        <Select model={modelFrom!}/>
        <Select model={modelTo!}/>
    </div> : <></>
}



