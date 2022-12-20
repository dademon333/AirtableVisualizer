import { AddMenu } from '../../components/add-menu/add-menu';
import { getConnectionNumber } from '../../redux/themes-data/selectors';
import { TypeConnections } from '../../types/types';
import { fetchThemes } from '../../redux/themes-data/api-actions';
import actions from '../../redux/themes-data/themes-data';

export const getAddMenu = (props: TypeConnections[]) => {
  const names = props.map((p) => p.child_column_name);

  return <AddMenu
    names={names}
    getConnectionNumber={getConnectionNumber}
    changeConnectionNumber={actions.changeConnectionNumber}
    fetchData={fetchThemes}
  />;
};