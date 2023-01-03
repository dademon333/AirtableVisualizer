import { useState } from 'react';
import { Modal } from 'react-bootstrap';
import { Entity } from '../types/types';

type WrapperFirstColElementProps = {
  entity: Entity;
  items: JSX.Element[][];
  column_names: string[];
}

export const WrapperFirstColElement = ({entity, items, column_names}: WrapperFirstColElementProps): JSX.Element => {
  const [showModal, setShowModal] = useState<boolean>(false);
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
                <div className='modal-block' key={`${elements}-${index}`}>
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
