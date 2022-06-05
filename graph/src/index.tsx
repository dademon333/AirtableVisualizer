import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { Provider } from 'react-redux';
import store from './libs/redux/store';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
  root.render(
      <Provider store={store}>
          <App />
      </Provider>
  );
} else {
  root.render(
    <React.StrictMode>
      <Provider store={store}>
          <App />
      </Provider>
    </React.StrictMode>
  );
}


//<React.StrictMode>
//</React.StrictMode>