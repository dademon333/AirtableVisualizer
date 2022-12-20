import { AddMenu } from '../../components/add-menu/add-menu';
import { getConnectionNumber } from './selectors';
import { TypeConnections } from '../../types/types';
import { fetchTargets } from './api-actions';
import actions from './targets-data';

export const getAddMenu = (props: TypeConnections[]) => {
  const names = props.map((p) => p.child_column_name);

  return <AddMenu
    names={names}
    getConnectionNumber={getConnectionNumber}
    changeConnectionNumber={actions.changeConnectionNumber}
    fetchData={fetchTargets}
  />;
};