import SelectModel from '../../models/select/select.model';
import './styles.css';
import { ReactComponent as Minus } from '../../assets/minus.svg';
import { useEffect, useState } from 'react';

export default function Select<T>(props: { model: SelectModel<T> }) {
    //const [model] = useState(props.model);
    const [value, setValue] = useState('0');
    const onSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        props.model.setSelectedItemById(e.target.value);
        setValue(e.target.value);
    };

    useEffect(() => {
        const defaultValue = props.model.Items.some(el => el.id === value) ? value : '0';
        setValue(defaultValue);
    }, [props.model.SelectedItem]);

    const onDeleteClick = () => {
        props.model.emitOnDelete();
    };

    return (
        <div className='select-wrapper'>
            <select className='select' onChange={e => onSelectChange(e)} value={value}>
                <option hidden disabled value={'0'}>{props.model.options?.placeholder || 'Выберите'}</option>
                {props.model.Items.map(item => <option value={item.id} key={item.id}>{item.name.length > 20 ? item.name.substring(0, 20) + '...' : item.name}</option>)}
            </select>
            {props.model.options?.isDeletable && <Minus className='minus' onClick={onDeleteClick}/>}
        </div>
    );
}