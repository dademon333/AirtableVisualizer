import SelectModel from '../../models/select/select.model';
import './styles.css';
import { ReactComponent as Minus } from '../../assets/minus.svg';
import { useState } from 'react';

export default function Select<T>(props: { model: SelectModel<T> }) {

    const [model, setModel] = useState(props.model);

    const onSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        model.setSelectedItemById(e.target.value);
    };

    const onDeleteClick = () => {
        model.emitOnDelete();
    };

    const defaultValue = model.SelectedItem ? model.SelectedItem.id : 0;
    
    return (
        <div className='select-wrapper'>
            <select className='select' onChange={e => onSelectChange(e)} defaultValue={defaultValue}>
                <option hidden disabled value={0}>{model.options?.placeholder || 'Выберите'}</option>
                {model.Items.map(item => <option value={item.id} key={item.id}>{item.name.length > 20 ? item.name.substring(0, 20) + '...' : item.name}</option>)}
            </select>
            {model.options?.isDeletable && <Minus className='minus' onClick={onDeleteClick}/>}
        </div>
    );
}