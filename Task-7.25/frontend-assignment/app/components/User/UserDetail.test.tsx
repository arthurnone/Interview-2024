import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { UserNamespace } from '@/app/types/user';
import UserContext from '@/app/context/UserContext';
import UserDetail from './UserDetail';

const mockSetSelectedUser = jest.fn();
const mockAddUser = jest.fn();
const mockUpdateUser = jest.fn();

const selectedUser: UserNamespace.User = {
  id: 1,
  name: 'wang',
  avatar: 'https://i.pravatar.cc/300?u=wang-1',
  username: 'wang',
  email: 'test@wangpeifeng.com',
  phone: '111-111-111',
  website: 'www.test.com',
  company: 'Wang Studio',
  dateJoined: '2024-07-23',
};

const columns = [
  { id: 'name', label: 'Name', required: true },
  { id: 'email', label: 'Email', required: true },
  { id: 'phone', label: 'Phone', required: false },
  { id: 'company', label: 'Company', required: false },
  { id: 'website', label: 'Website', required: false },
];

const renderComponent = (mode: string) => {
  const contextValue: UserNamespace.UserContextProps = {
    users: [],
    selectedUser,
    setSelectedUser: mockSetSelectedUser,
    setUsers: jest.fn(),
    fetchUsers: jest.fn(),
    addUser: mockAddUser,
    updateUser: mockUpdateUser,
    delUser: jest.fn(),
  };

  return render(
    <UserContext.Provider value={contextValue}>
      <UserDetail mode={mode} />
    </UserContext.Provider>,
  );
};

describe('UserDetail Component', () => {
  it('renders correctly with selected user details', () => {
    const { container } = renderComponent('edit');

    console.log(container.innerHTML);

    expect(screen.getByText("wang's Detail")).toBeInTheDocument();
    expect(screen.getByDisplayValue('1')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Wang Studio')).toBeInTheDocument();
    expect(
      screen.getByDisplayValue('test@wangpeifeng.com'),
    ).toBeInTheDocument();
    expect(screen.getByDisplayValue('111-111-111')).toBeInTheDocument();
    expect(screen.getByDisplayValue('www.test.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('2024-07-23')).toBeInTheDocument();
  });

  it('calls setSelectedUser with null when close button is clicked', () => {
    renderComponent('edit');

    fireEvent.click(screen.getByText('Close'));
    expect(mockSetSelectedUser).toHaveBeenCalledWith(null);
  });

  it('calls addUser with selectedUser details when add button is clicked', () => {
    renderComponent('add');

    fireEvent.click(screen.getByText('Add'));
    expect(mockAddUser).toHaveBeenCalledWith(selectedUser);
  });

  it('calls updateUser with selectedUser details when submit button is clicked', () => {
    renderComponent('edit');

    fireEvent.click(screen.getByText('Submit'));
    expect(mockUpdateUser).toHaveBeenCalledWith(selectedUser);
  });

  it('shows error when required fields are empty', () => {
    const incompleteUser: UserNamespace.User = {
      ...selectedUser,
      username: '',
    };
    const contextValue: UserNamespace.UserContextProps = {
      users: [],
      selectedUser: incompleteUser,
      setSelectedUser: mockSetSelectedUser,
      setUsers: jest.fn(),
      fetchUsers: jest.fn(),
      addUser: mockAddUser,
      updateUser: mockUpdateUser,
      delUser: jest.fn(),
    };

    render(
      <UserContext.Provider value={contextValue}>
        <UserDetail mode="add" />
      </UserContext.Provider>,
    );

    fireEvent.click(screen.getByText('Add'));
  });

  it('does not render when selectedUser is null', () => {
    const contextValue: UserNamespace.UserContextProps = {
      users: [],
      selectedUser: null,
      setSelectedUser: mockSetSelectedUser,
      setUsers: jest.fn(),
      fetchUsers: jest.fn(),
      addUser: mockAddUser,
      updateUser: mockUpdateUser,
      delUser: jest.fn(),
    };

    const { container } = render(
      <UserContext.Provider value={contextValue}>
        <UserDetail mode="add" />
      </UserContext.Provider>,
    );

    expect(container.firstChild).toBeNull();
  });
});
