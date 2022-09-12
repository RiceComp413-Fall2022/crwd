import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

import '@testing-library/jest-dom';

test('includes crwd.io title', () => {
  render(<App />);
  const titleElement = screen.getByText(/crwd.io/i); // Look for crwd with regex (ignoring case)
  expect(titleElement).toBeInTheDocument();
});
