import { FormEvent, useRef } from 'react';
import { Modal, Form, Button } from 'react-bootstrap';
import { useAppDispatch } from '../../hooks';
import { EntityType } from '../../const';
import { postEntity, deleteEntity } from '../../redux/change-data/api-actions';

type AddDataWindowProps = {
  showModal: boolean;
  onHide: React.Dispatch<React.SetStateAction<boolean>>;
}

export const AddDataWindow = ({ showModal, onHide }: AddDataWindowProps): JSX.Element => {
  const dispatch = useAppDispatch();
  const inputRef = useRef<HTMLInputElement | null>(null);
  const selectRef = useRef<HTMLSelectElement | null>(null);

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (inputRef.current && selectRef.current) {
      /* dispatch(postEntity({
        name: inputRef.current.value,
        type: selectRef.current.value,
        size: 'medium',
        description: '',
        study_time: 0
      })); */
    }
  }

  return (
    <Modal show={showModal} onHide={() => onHide(false)}>
      <Modal.Header closeButton>
        Добавление в таблицу
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={onSubmit}>
          <Form.Group className='mb-3'>
            <Form.Control type='text' placeholder='Название' ref={inputRef} />
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
          <Button type='submit'>Добавить</Button>
        </Form> 
      </Modal.Body>
    </Modal>
  );
}
