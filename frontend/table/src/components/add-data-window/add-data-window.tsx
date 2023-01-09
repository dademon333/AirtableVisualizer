import { FormEvent, useRef } from 'react';
import { Modal, Form, Button, Spinner } from 'react-bootstrap';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { EntityType } from '../../const';
import { postEntity } from '../../redux/change-data/api-actions';
import actions from '../../redux/change-data/change-data';
import { getIsLoading, getIsAddDataModalOpen } from '../../redux/change-data/selectors';

type AddDataWindowProps = {
  entityType: EntityType;
}

export const AddDataWindow = ({ entityType }: AddDataWindowProps): JSX.Element => {
  const dispatch = useAppDispatch();
  const inputRef = useRef<HTMLInputElement | null>(null);
  const selectRef = useRef<HTMLSelectElement | null>(null);

  const isLoading = useAppSelector(getIsLoading);
  const isAddDataModalOpen = useAppSelector(getIsAddDataModalOpen);

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (inputRef.current && selectRef.current) {
      dispatch(postEntity({
        name: inputRef.current.value,
        type: selectRef.current.value,
        size: 'medium',
        description: '',
        study_time: 0
      }));
    };
  };

  return (
    <Modal show={isAddDataModalOpen} onHide={() => dispatch(actions.changeAddDataModalOpen(false))}>
      <Modal.Header closeButton>
        Добавление в таблицу
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={onSubmit}>
          <Form.Group className='mb-3'>
            <Form.Control type='text' placeholder='Название' ref={inputRef} required />
          </Form.Group>
          <Form.Group className='mb-3'>
            <Form.Select ref={selectRef}>
              <option value={EntityType.Course}>Курс</option>
              <option value={EntityType.Theme}>Тема</option>
              <option value={EntityType.Knowledge}>Знание</option>
              <option value={EntityType.Quantum}>Квант</option>
              <option value={EntityType.Target}>Цель</option>
            </Form.Select>
          </Form.Group>
          <Button type='submit'>
            {
              isLoading
              ? <Spinner animation='border' size='sm' />
              : 'Добавить'
            }
          </Button>
        </Form> 
      </Modal.Body>
    </Modal>
  );
}
