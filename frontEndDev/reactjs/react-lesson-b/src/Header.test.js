import React from 'react';
import { render } from '@testing-library/react';
import Header from './Header';


test('test of Header', () => {
    const { getByText } = render(<Header />);
});