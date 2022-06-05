import SelectModel from '../../models/select/select.model';
import './styles.css';

export default function Select<T>(props: { model: SelectModel<T> }) {
    const onSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        console.log(e.target.value);
        props.model.setSelectedItemById(e.target.value);
    };


    return (
        <div className='select-wrapper'>
            <select className='select' onChange={e => onSelectChange(e)}>
                {props.model.Items.map(item => <option value={item.id} key={item.id}>{item.name}</option>)}
            </select>
        </div>
    );
}