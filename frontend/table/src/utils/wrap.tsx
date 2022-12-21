export const wrapFirstColElement = (name: string): JSX.Element => (
  <div className='first-column-element' title={name}>{name}</div>
);


export const wrapSecondColElement = (name: string, index: number): JSX.Element => (
  <div className='secondary-column-element' key={`${name}-${index}`}>{name}</div>
);

export const wrapSecondColElements = (items: JSX.Element[]): JSX.Element => (
  <div className='secondary-column-elements'>{items}</div>
);
