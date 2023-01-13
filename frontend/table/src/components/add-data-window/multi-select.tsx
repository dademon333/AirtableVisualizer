import { useRef } from 'react';
import { Form } from 'react-bootstrap';
import Select, { SelectInstance } from 'react-select';
import { useAppDispatch } from '../../hooks';
import { SelectConnectWithOption } from '../../types/types';
import actions from '../../redux/change-data/change-data';

type MultiSelectProps = {
  data: SelectConnectWithOption[];
  entityTypeName: string;
}

export const MultiSelect = ({ data, entityTypeName }: MultiSelectProps): JSX.Element => {
  const dispatch = useAppDispatch();

  const selectConnectWithRef = useRef<SelectInstance<SelectConnectWithOption> | null>(null);

  const handleChange = (newValue: any) => {
    if (newValue) {
      dispatch(actions.updateChosenEntities({
        name: entityTypeName,
        entities: newValue
      }));
    }
  };

  return (
    <Form.Group className='mb-3'>
      <Form.Label>{entityTypeName}</Form.Label>
      <Select
        options={data}
        ref={selectConnectWithRef}
        isMulti
        placeholder='Связать с ...'
        closeMenuOnSelect={false}
        onChange={handleChange}
      />
    </Form.Group>
  );
};
