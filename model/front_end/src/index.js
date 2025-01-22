// src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';  // App.js를 임포트
// import './styles/index.css';  // 스타일 파일이 있으면 임포트

const root = ReactDOM.createRoot(document.getElementById('root')); // root 요소 가져오기
root.render(<App />);  // App 컴포넌트 렌더링
