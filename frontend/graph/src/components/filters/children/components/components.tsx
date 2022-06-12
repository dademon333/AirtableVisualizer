import { useDispatch, useSelector } from 'react-redux';
import EntityType from '../../../../enums/entity-type.enum';
import ISelect from '../../../../interfaces/control/select.interface';
import SelectModel from '../../../../models/select/select.model';
import { setComponentType, addComponentEntity, setComponentEntities, removeComponentEntity, setSetType, IVisibleEntity, setVisibleEntites } from '../../../../redux/slices/filter.slice';
import Select from '../../../select/select';
import './styles.css';
import { ReactComponent as Plus } from '../../../../assets/plus.svg';
import store from '../../../../redux/store';
import { useEffect, useState } from 'react';
import { first, map } from 'rxjs';
import SetType from '../../../../enums/set-type.enum';
import INode from '../../../../interfaces/graph/node.interface';

export default function Components() {

    const [componentTypeModel] = useState(new SelectModel<EntityType>(items));
    const [setTypeModel] = useState(new SelectModel<SetType>(setTypeItems, {}, setTypeItems[0]));
    const [controls, setControls] = useState<Array<SelectModel<string>>>([]);

    const onComponentTypeChange = (item: ISelect<EntityType>) => {
        dispatch(setComponentType(item.value!));
        dispatch(setComponentEntities([]));
        setControls([]);
    };

    const onSetTypeChange = (item: ISelect<SetType>) => {
        dispatch(setSetType(item.value!));
    };
    
    useEffect(() => {
        componentTypeModel.OnItemChange.subscribe(onComponentTypeChange);
        setTypeModel.OnItemChange.subscribe(onSetTypeChange);
    }, []);

    const dispatch = useDispatch();

    const setValues = (els: Array<SelectModel<string>>) => {
        const newValues = els.filter(el => el.SelectedItem !== null).map(el => el.SelectedItem?.id!);
        dispatch(setComponentEntities(newValues));
        // const visibleNodes = setTypeModel.SelectedItem?.value === SetType.Union || controls.length == 1 
        // ? getVisibleNodesForUnionSetType(newValues)
        // : getVisibleEntitiesForIntersectionSetType(newValues);
        // dispatch(setVisibleEntites(visibleNodes));
    };

    const onPlusClick = () => {

        const entities = Object.entries(store.getState().entitiesConnections.entities)
        .filter(el => el[1].type === componentTypeModel.SelectedItem?.value)
        .map(el => {
            const res: ISelect<EntityType> = {
                id: el[0],
                name: el[1].name
            };

            return res;
        });

        const newModel = new SelectModel<string>(entities, { isDeletable: true });
        setControls(prev => [...prev, newModel]);
        
    };

    return (<div className="components">
        <h2 className='components-title'>КОМПОНЕНТЫ</h2>
        <Select model={componentTypeModel}/>
        {componentTypeModel.SelectedItem && <Plus className='plus' onClick={() => onPlusClick()}/>}
        {controls.map((model, i) => {
            model.OnDelete.pipe(
                first(),
                map(() => {
                    setControls(prev => {
                        setValues(prev.filter(el => el.id !== model.id));
                        return prev.filter(el => el.id !== model.id);
                    });
                    
                })
            ).subscribe();

            model.OnItemChange.pipe(
                map(_ => {
                    setValues(controls);
                })
            ).subscribe();

            
            return  <Select key={model.id} model={model}/>;
        })}
        {controls.length > 1 && <Select model={setTypeModel}/>}
    </div>)
}

const items: ISelect<EntityType>[] = [
    {id: '1', name: 'Курс', value: EntityType.Course },
    {id: '2', name: 'Тема', value: EntityType.Theme },
    {id: '3', name: 'Знание', value: EntityType.Knowledge },
    {id: '4', name: 'Квантум', value: EntityType.Quantum },
    {id: '5', name: 'Цель', value: EntityType.Target },
    {id: '6', name: 'Метрика', value: EntityType.Metric },
    {id: '7', name: 'Задание', value: EntityType.Task },
    {id: '8', name: 'Деятельность', value: EntityType.Activity },
    {id: '9', name: 'Навык', value: EntityType.Skill },
    {id: '10', name: 'Компетенция', value: EntityType.Competence },
    {id: '11', name: 'Профессия', value: EntityType.Profession },
    {id: '12', name: 'Компетенция СУОС', value: EntityType.SuosCompetence },
];

const setTypeItems: ISelect<SetType>[] = [
    {id: '1', name: 'Объединение', value: SetType.Union },
    {id: '2', name: 'Пересечение', value: SetType.Intersection },
];

// const getVisibleNodesForUnionSetType = (entitesToShow: string[]): INode[] => {

//     if (entitesToShow.length === 0) {
//         return [];
//     }

//     const allNodes = store.getState().entitiesConnections.connections;
//     return allNodes.filter(el => {
//         const res = entitesToShow.includes(el.id) || el.connectedNodes.some(node => entitesToShow.includes(node.id));
//         return res;
//     });
// }

// const getVisibleEntitiesForIntersectionSetType = (entitesToShow: string[]): INode[] => {
//     if (entitesToShow.length === 0) {
//         return [];
//     }

//     const allNodes = store.getState().graph.nodes;

//     return allNodes.filter(el => {
//         const res = entitesToShow.includes(el.id) || el.connectedNodes.filter(node => entitesToShow.includes(node.id)).length >= entitesToShow.length;;
//         return res;
//     });
// }