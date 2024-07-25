import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { UserNamespace } from '@/app/types/user';
import UserContext from '@/app/context/UserContext';
import UserList from './UserList';

const mockSetSelectedUser = jest.fn();
const mockFetchUsers = jest.fn();

const users: UserNamespace.User[] = [
  {
    id: 1,
    name: 'Wang',
    avatar: 'https://i.pravatar.cc/300?u=wang',
    username: 'wang',
    email: 'wang@example.com',
    phone: '123-456-7890',
    website: 'www.wang.com',
    company: 'Wang Studio',
    dateJoined: '2023-01-01',
  },
  {
    id: 2,
    name: 'Wang 2',
    avatar: 'https://i.pravatar.cc/300?u=wang2',
    username: 'wang2',
    email: 'wang2@example.com',
    phone: '987-654-3210',
    website: 'www.wang2.com',
    company: 'Wang2 Co',
    dateJoined: '2023-02-01',
  },
];

const columns = [
  { id: 'email', label: 'Email', required: true },
  { id: 'phone', label: 'Phone', required: true },
  { id: 'website', label: 'Website', required: false },
  { id: 'company', label: 'Company', required: false },
];

const renderComponent = () => {
  const contextValue: UserNamespace.UserContextProps = {
    users,
    selectedUser: null,
    setSelectedUser: mockSetSelectedUser,
    setUsers: jest.fn(),
    fetchUsers: mockFetchUsers,
    addUser: jest.fn(),
    updateUser: jest.fn(),
    delUser: jest.fn(),
  };

  return render(
    <UserContext.Provider value={contextValue}>
      <UserList />
    </UserContext.Provider>,
  );
};

describe('UserList Component', () => {
  it('renders correctly with users data', () => {
    renderComponent();

    // Check for table headers
    expect(screen.getByText('ID')).toBeInTheDocument();
    expect(screen.getByText('Avatar')).toBeInTheDocument();
    expect(screen.getByText('Username')).toBeInTheDocument();
    expect(screen.getByText('Email')).toBeInTheDocument();
    expect(screen.getByText('Phone')).toBeInTheDocument();
    expect(screen.getByText('Website')).toBeInTheDocument();
    expect(screen.getByText('Company')).toBeInTheDocument();

    // Check for user data
    users.forEach(user => {
      expect(screen.getByText(user.username)).toBeInTheDocument();
      expect(screen.getByText(user.email)).toBeInTheDocument();
      expect(screen.getByText(user.phone)).toBeInTheDocument();
      expect(screen.getByText(user.website)).toBeInTheDocument();
      expect(screen.getByText(user.company)).toBeInTheDocument();
    });
  });

  it('calls setSelectedUser and opens UserDetail on add button click', () => {
    renderComponent();

    fireEvent.click(screen.getByText(/Add User/i));
    expect(mockSetSelectedUser).toHaveBeenCalledWith({
      id: 0,
      name: 'New User',
      avatar: '',
      username: '',
      email: '',
      phone: '',
      website: '',
      company: '',
      dateJoined: '',
    });
  });

  it('calls setSelectedUser and opens UserDetail on edit button click', () => {
    renderComponent();

    const editButtons = screen.getAllByRole('button', { name: /Edit/i });
    fireEvent.click(editButtons[0]); // Click the edit button for the first user

    expect(mockSetSelectedUser).toHaveBeenCalledWith(users[0]);
  });

  it('calls setSelectedUser and opens UserDelete on delete button click', () => {
    renderComponent();

    const deleteButtons = screen.getAllByRole('button', { name: /Delete/i });
    fireEvent.click(deleteButtons[0]); // Click the delete button for the first user

    expect(mockSetSelectedUser).toHaveBeenCalledWith(users[0]);
  });

  it('calls fetchUsers on page change', () => {
    renderComponent();

    fireEvent.click(screen.getByRole('button', { name: /Next page/i }));
    expect(mockFetchUsers).toHaveBeenCalledWith(2);
  });
});
