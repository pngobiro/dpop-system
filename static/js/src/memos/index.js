// static/js/src/memos/index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import MemoApp from './MemoApp';

const container = document.getElementById('memo-app');
const root = createRoot(container);
root.render(<MemoApp />);