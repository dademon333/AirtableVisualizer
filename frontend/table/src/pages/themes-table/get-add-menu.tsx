import { AddMenu } from '../../components/add-menu/add-menu';
import { getConnectionNumber } from '../../redux/themes-data/selectors';
import { TypeConnections } from '../../types/types';
import { fetchThemes } from '../../redux/themes-data/api-actions';
import actions from '../../redux/themes-data/themes-data';
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
    fetchData={fetchThemes}
  />;
};