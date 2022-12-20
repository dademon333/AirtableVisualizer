import { AddMenu } from '../../components/add-menu/add-menu';
import { getConnectionNumber } from '../../redux/targets-data/selectors';
import { TypeConnections } from '../../types/types';
import { fetchTargets } from '../../redux/targets-data/api-actions';
import actions from '../../redux/targets-data/targets-data';

export const getAddMenu = (props: TypeConnections[]) => {
  const names = props.map((p) => p.child_column_name);

  return <AddMenu
    names={names}
    getConnectionNumber={getConnectionNumber}
    changeConnectionNumber={actions.changeConnectionNumber}
    fetchData={fetchTargets}
  />;
};