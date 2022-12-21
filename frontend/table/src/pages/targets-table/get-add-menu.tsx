import { AddMenu } from '../../components/add-menu/add-menu';
import { getConnectionNumber } from '../../redux/targets-data/selectors';
import { TypeConnections } from '../../types/types';
import { fetchTargets } from '../../redux/targets-data/api-actions';
import actions from '../../redux/targets-data/targets-data';
import { EntityType } from '../../const';

export const getAddMenu = (connections: TypeConnections[], type: EntityType): JSX.Element => {
  const names = connections.map((p) => {
    if (p.parent_type === type) {
      return p.child_column_name;
    } else {
      return p.parent_column_name;
    }
  });

  return <AddMenu
    names={names}
    getConnectionNumber={getConnectionNumber}
    changeConnectionNumber={actions.changeConnectionNumber}
    fetchData={fetchTargets}
  />;
};