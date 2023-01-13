import { FormEvent, useRef } from 'react';
import { Modal, Form, Button, Spinner } from 'react-bootstrap';
import Select, { SelectInstance, SingleValue } from 'react-select';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { EntityType } from '../../const';
import { SelectConnectWithOption } from '../../types/types';
import { postEntity, fetchRelatedEntityTypes, postEntityWithRelatedEntities } from '../../redux/change-data/api-actions';
import actions from '../../redux/change-data/change-data';
import {
  getIsLoading,
  getIsAddDataModalOpen,
  getRelatedEntities,
  getRelatedEntityTypeNames,
  getIsRelatedEntitiesLoading,
  getChosenEntities,
} from '../../redux/change-data/selectors';
import { MultiSelect } from './multi-select';

type SelectEntityOption = {
  value: EntityType;
  label: string;
}

export const AddDataWindow = (): JSX.Element => {
  const dispatch = useAppDispatch();

  const inputRef = useRef<HTMLInputElement | null>(null);
  const selectEntityTypeRef = useRef<SelectInstance<SelectEntityOption> | null>(null);

  const isLoading = useAppSelector(getIsLoading);
  const isAddDataModalOpen = useAppSelector(getIsAddDataModalOpen);
  const relatedEntities = useAppSelector(getRelatedEntities);
  const relatedEntityTypeNames = useAppSelector(getRelatedEntityTypeNames);
  const isRelatedEntitiesLoading = useAppSelector(getIsRelatedEntitiesLoading);
  const chosenEntities = useAppSelector(getChosenEntities);

  const selectEntityData: SelectEntityOption[] = [
    { value: EntityType.Course, label: 'Курс' },
    { value: EntityType.Theme, label: 'Тема' },
    { value: EntityType.Knowledge, label: 'Знание' },
    { value: EntityType.Quantum, label: 'Квант' },
    { value: EntityType.Target, label: 'Цель' },
  ];

  let selectConnectWithData: SelectConnectWithOption[][] = [];
  if (relatedEntities.length !== 0) {
    relatedEntities.forEach((e) => {
      selectConnectWithData.push(e.map((item) => (
        {
          value: item,
          label: item.name
        }
      )));
    });
  };

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (inputRef.current && selectEntityTypeRef.current) {
      const name = inputRef.current.value;
      const type = selectEntityTypeRef.current.getValue()[0].value;

      if (!chosenEntities) {
        dispatch(postEntity({
          name,
          type,
          size: 'medium',
          description: '',
          study_time: 0
        }));
      } else {
        dispatch(postEntityWithRelatedEntities({
          entity: {
            name,
            type,
            size: 'medium',
            description: '',
            study_time: 0
          },
          relatedEntities: chosenEntities
        }));
      };
    };
  };

  const handleSelectEntityType = (newValue: SingleValue<SelectEntityOption>) => {
    newValue && dispatch(fetchRelatedEntityTypes(newValue.value));
  };

  const handleHide = () => {
    dispatch(actions.changeAddDataModalOpen(false));
    dispatch(actions.clearRelatedEntities());
  };

  return (
    <Modal show={isAddDataModalOpen} onHide={handleHide}>
      <Modal.Header closeButton>
        Добавление в таблицу
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={onSubmit}>
          <Form.Group className='mb-3'>
            <Form.Control type='text' placeholder='Название' ref={inputRef} required />
          </Form.Group>
          <Form.Group className='mb-3'>
            <Select
              options={selectEntityData}
              ref={selectEntityTypeRef}
              onChange={handleSelectEntityType}
              name='selectEntity'
              placeholder='Тип'
            />
          </Form.Group>
          {
            isRelatedEntitiesLoading
            ? <Spinner animation='border' className='related-loading' />
            : 
            selectConnectWithData.map((data, index) => (
              <MultiSelect 
                key={`${data[0]}-${index}`}
                data={data}
                entityTypeName={relatedEntityTypeNames[index]}
              />
            ))
          }
          {
            isLoading
            ? <Button disabled><Spinner animation='border' size='sm' /></Button>
            : <Button type='submit'>Добавить</Button>
          }
        </Form>
      </Modal.Body>
    </Modal>
  );
}
