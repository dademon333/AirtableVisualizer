import SelectModel from '../../models/select/select.model';
import './styles.css';

export default function Select<T>(props: { model: SelectModel<T> }) {
    const onSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        props.model.setSelectedItemById(e.target.value);
    };
    
    return (
        <div className='select-wrapper'>
            <select className='select' onChange={e => onSelectChange(e)} defaultValue={1}>
                <option hidden disabled value={1}>{props.model.options?.placeholder || 'Выберите'}</option>
                {props.model.Items.map(item => <option value={item.id} key={item.id}>{item.name}</option>)}
            </select>
        </div>
    );
}