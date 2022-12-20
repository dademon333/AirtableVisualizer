import { AddMenu } from '../../components/add-menu/add-menu';
import { getConnectionNumber } from '../../redux/quntums-data/selectors';
import { TypeConnections } from '../../types/types';
import { fetchQuauntums } from '../../redux/quntums-data/api-actions';
import actions from '../../redux/quntums-data/quantums-data';

export const getAddMenu = (props: TypeConnections[]) => {
  const names = props.map((p) => p.child_column_name);

  return <AddMenu
    names={names}
    getConnectionNumber={getConnectionNumber}
    changeConnectionNumber={actions.changeConnectionNumber}
    fetchData={fetchQuauntums}
  />;
};