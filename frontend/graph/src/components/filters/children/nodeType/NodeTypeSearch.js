import { ReactComponent as Arrow } from '../../../../assets/arrow.svg';
import { ReactComponent as Cross } from '../../../../assets/cross.svg';
import Select from '../../../select/select';
import Components from '../components/components';
import "./nodeTypeSearch.css"

const NodeTypeSearch = ({onClickArrow}) => {
  return (
    <div className="filters">
      <div className="controls">
      <Arrow onClick={() => onClickArrow()}/>
      <Cross/>
      </div>
            <h2 className="filters-title">Типы вершин</h2>
            <Components/>
      </div>
  )
}

export default NodeTypeSearch

