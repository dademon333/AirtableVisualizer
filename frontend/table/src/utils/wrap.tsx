import { useState } from 'react';
import { Modal } from 'react-bootstrap';
import { Course, Entity } from '../types/types';

type WrapperFirstColElementProps = {
  item: Entity | Course;
}

export const WrapperFirstColElement = ({item}: WrapperFirstColElementProps): JSX.Element => {
  const [showModal, setShowModal] = useState<boolean>(false);
  return (
    <>
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header>
          {item.id}
        </Modal.Header>
      </Modal>
      <div className='first-column-element' onClick={() => setShowModal(true)} title={item.name}>{item.name}</div>
    </>
  );
};

export const wrapSecondColElement = (name: string, index: number): JSX.Element => (
  <div className='secondary-column-element' key={`${name}-${index}`}>{name}</div>
);

export const wrapSecondColElements = (items: JSX.Element[]): JSX.Element => (
  <div className='secondary-column-elements'>{items}</div>
);
