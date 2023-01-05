import { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';
import { Entity } from '../types/types';
import { useAppDispatch } from '../hooks';
import { deleteEntity } from '../redux/change-data/api-actions';

type WrapperFirstColElementProps = {
  entity: Entity;
  items: JSX.Element[][];
  column_names: string[];
}

export const WrapperFirstColElement = ({entity, items, column_names}: WrapperFirstColElementProps): JSX.Element => {
  const dispatch = useAppDispatch();
  const [showModal, setShowModal] = useState<boolean>(false);
  
  const onDeleteHandler = () => {
    dispatch(deleteEntity({id: entity.id!, entityType: entity.type!}));
    setShowModal(false);
  }

  return (
    <>
      <Modal show={showModal} onHide={() => setShowModal(false)} size='lg'>
        <Modal.Header closeButton>
          {entity.name.toUpperCase()}
        </Modal.Header>
        <Modal.Body>
          {
            items.map((elements, index) => {
              return (
                <div className='modal-block' key={`${elements[index]}-${index}`}>
                  <div className='modal-block__column-name'>
                    { column_names[index] }
                  </div>
                  { elements.length === 0
                    ? 'Нет даных'
                    : <div className='modal-block__elements'>{elements}</div>
                  }
                </div>
              );
            })
          }
        </Modal.Body>
        <Modal.Footer>
          <Button variant='danger' onClick={onDeleteHandler}>Удалить</Button>
        </Modal.Footer>
      </Modal>
      <div className='first-column-element' onClick={() => setShowModal(true)} title={entity.name}>{entity.name}</div>
    </>
  );
};

export const wrapSecondColElement = (name: string, index: number): JSX.Element => (
  <div className='secondary-column-element' key={`${name}-${index}`}>{name}</div>
);

export const wrapSecondColElements = (items: JSX.Element[]): JSX.Element => (
  <div className='secondary-column-elements'>{items}</div>
);
