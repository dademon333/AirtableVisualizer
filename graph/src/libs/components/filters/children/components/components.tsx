import ISelect from '../../../../interfaces/select/select.interface';
import SelectModel from '../../../../models/select/select.model';
import Select from '../../../select/select';
import './styles.css';


export default function Components() {
    const items: ISelect<string>[] = [{id: '1', name: 'Курс'}, {id: '2', name: 'Знание'}];
    const selectModel = new SelectModel<string>(items);
    return <div className="components">
        <h2>Компоненты</h2>
        <Select model={selectModel}/>
    </div>
}