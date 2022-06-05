import { useDispatch } from 'react-redux';
import EntityType from '../../../../enums/entity-type.enum';
import ISelect from '../../../../interfaces/control/select.interface';
import SelectModel from '../../../../models/select/select.model';
import { setComponentType } from '../../../../redux/slices/filter.slice';
import Select from '../../../select/select';
import './styles.css';


export default function Components() {
    const dispatch = useDispatch();
    const onItemChange = (item: ISelect<EntityType>) => {
        dispatch(setComponentType(item.value!));
    }

    const selectModel = new SelectModel<EntityType>(items, onItemChange);
    return <div className="components">
        <h2>Компоненты</h2>
        <Select model={selectModel}/>
    </div>
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