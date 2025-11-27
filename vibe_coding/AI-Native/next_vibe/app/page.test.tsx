import { render, screen } from '@testing-library/react';
import Home from './page';

describe('Home', () => {
  it('renders without crashing', () => {
    render(<Home />);
  });

  it('displays the Next.js logo', () => {
    render(<Home />);
    const logo = screen.getByAltText('Next.js logo');
    expect(logo).toBeInTheDocument();
  });

  it('displays the main heading', () => {
    render(<Home />);
    const heading = screen.getByRole('heading', { name: /To get started, edit the page.tsx file./i });
    expect(heading).toBeInTheDocument();
  });

  it('displays the "로또" button', () => {
    render(<Home />);
    const lottoButton = screen.getByRole('button', { name: /로또/i });
    expect(lottoButton).toBeInTheDocument();
  });
});
