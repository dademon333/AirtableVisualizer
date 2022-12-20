import { AddMenu } from '../../components/add-menu/add-menu';
import { getConnectionNumber } from '../../redux/courses-data/selectors';
import { TypeConnections } from '../../types/types';
import { fetchCourses } from '../../redux/courses-data/api-actions';
import actions from '../../redux/courses-data/courses-data';

export const getAddMenu = (props: TypeConnections[]) => {
  const names = props.map((p) => p.child_column_name);

  return <AddMenu
    names={names}
    getConnectionNumber={getConnectionNumber}
    changeConnectionNumber={actions.changeConnectionNumber}
    fetchData={fetchCourses}
  />;
};