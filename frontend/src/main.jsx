import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { CssBaseline } from '@mui/material';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import {BrowserRouter} from "react-router-dom";

import imgs from "./img/imgs.js";

const faviconUrl = imgs[1];

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
      <BrowserRouter>
          <CssBaseline/>
          <App />
      </BrowserRouter>
  </React.StrictMode>,
)