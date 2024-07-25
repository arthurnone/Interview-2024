import { useCallback } from 'react';
import { UserNamespace } from '@/app/types/user';
import { API_BASE_URL } from '@/app/constants/constants';

/**
 * Custom hook to manage user actions such as fetching, adding, updating, and deleting users.
 *
 * @param setUsers - The state setter function to update the list of users.
 * @returns An object containing functions to fetch users, add a user, update a user, and delete a user.
 */
export const useUserActions = (
  setUsers: React.Dispatch<React.SetStateAction<UserNamespace.User[]>>,
) => {
  /**
   * Fetches users from the API and updates the state.
   *
   * @param page - The page number to fetch users from.
   */
  const fetchUsers = useCallback(
    async (page: number) => {
      const res = await fetch(`${API_BASE_URL}/api/user?page=${page}`);
      const data = await res.json();
      setUsers(data.users);
    },
    [setUsers],
  );

  /**
   * Adds a new user to the API and updates the state.
   *
   * @param user - The user object to be added.
   */
  const addUser = useCallback(
    async (user: UserNamespace.User) => {
      const res = await fetch(`${API_BASE_URL}/api/user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
      });

      if (res.ok) {
        const response = await res.json();
        setUsers(prevUsers => [...prevUsers, response.user]);
      } else {
        console.error('Failed to add user');
      }
    },
    [setUsers],
  );

  /**
   * Updates an existing user in the API and updates the state.
   *
   * @param user - The user object to be updated.
   */
  const updateUser = useCallback(
    async (user: UserNamespace.User) => {
      const res = await fetch(`${API_BASE_URL}/api/user`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
      });

      if (res.ok) {
        const response = await res.json();
        const updatedUser = response.user;
        setUsers(prevUsers =>
          prevUsers.map(u => (u.id === updatedUser.id ? updatedUser : u)),
        );
      } else {
        console.error('Failed to update user');
      }
    },
    [setUsers],
  );

  /**
   * Deletes a user from the API and updates the state.
   *
   * @param id - The ID of the user to be deleted.
   */
  const delUser = useCallback(
    async (id: number) => {
      const res = await fetch(`${API_BASE_URL}/api/user`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id }),
      });

      if (res.ok) {
        setUsers(prevUsers => prevUsers.filter(user => user.id !== id));
      } else {
        console.error('Failed to delete user');
      }
    },
    [setUsers],
  );

  return {
    fetchUsers,
    addUser,
    updateUser,
    delUser,
  };
};
