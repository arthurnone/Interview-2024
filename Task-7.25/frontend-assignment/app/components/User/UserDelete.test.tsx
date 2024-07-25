import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { prettyDOM } from '@testing-library/dom';
import { UserNamespace } from '@/app/types/user';
import UserContext from '@/app/context/UserContext';
import UserDelete from './UserDelete';

const mockSetOpen = jest.fn();
const mockDelUser = jest.fn();

const renderComponent = (contextValue: UserNamespace.UserContextProps) => {
  return render(
    <UserContext.Provider value={contextValue}>
      <UserDelete open={true} setOpen={mockSetOpen} />
    </UserContext.Provider>,
  );
};

describe('UserDelete Component', () => {
  const contextValue: UserNamespace.UserContextProps = {
    users: [],
    selectedUser: {
      avatar: 'https://i.pravatar.cc/300?u=wang-1',
      company: 'Wang Studio',
      dateJoined: '2024/07/23',
      email: 'test@wangpeifeng.com',
      id: 1,
      name: 'wang',
      phone: '111-111-111',
      username: 'wang',
      website: 'www.test.com',
    },
    setSelectedUser: jest.fn(),
    setUsers: jest.fn(),
    fetchUsers: jest.fn(),
    addUser: jest.fn(),
    updateUser: jest.fn(),
    delUser: mockDelUser,
  };

  it('renders correctly with given context', () => {
    const { container } = renderComponent(contextValue);

    console.log(prettyDOM(container));
  });

  it('calls setOpen with false when cancel button is clicked', () => {
    renderComponent(contextValue);

    fireEvent.click(screen.getByText('Cancel'));
    expect(mockSetOpen).toHaveBeenCalledWith(false);
  });

  it('throws an error when used without UserContext', () => {
    const consoleErrorSpy = jest
      .spyOn(console, 'error')
      .mockImplementation(() => {});
    expect(() =>
      render(<UserDelete open={true} setOpen={mockSetOpen} />),
    ).toThrow('UserList must be used within a UserProvider');
    consoleErrorSpy.mockRestore();
  });
});
