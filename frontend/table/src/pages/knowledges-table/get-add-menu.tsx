import { AddMenu } from '../../components/add-menu/add-menu';
import { getConnectionNumber } from '../../redux/knowledges-data/selectors';
import { TypeConnections } from '../../types/types';
import { fetchKnowledges } from '../../redux/knowledges-data/api-actions';
import actions from '../../redux/knowledges-data/knowledges-data';

export const getAddMenu = (props: TypeConnections[]) => {
  const names = props.map((p) => p.child_column_name);

  return <AddMenu
    names={names}
    getConnectionNumber={getConnectionNumber}
    changeConnectionNumber={actions.changeConnectionNumber}
    fetchData={fetchKnowledges}
  />;
};