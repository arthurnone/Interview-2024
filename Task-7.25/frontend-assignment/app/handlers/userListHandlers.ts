import { UserNamespace } from '@/app/types/user';
import { Dispatch, SetStateAction } from 'react';

/**
 * Custom hook to handle user list actions such as changing the page and selecting a user.
 *
 * @param setMode - The state setter function to update the mode.
 * @param setSelectedUser - The state setter function to update the selected user.
 * @param setShowDel - The state setter function to show or hide the delete confirmation.
 * @param setPage - The state setter function to update the current page.
 * @param fetchUsers - The function to fetch users for a given page.
 * @returns An object containing functions to change the page and select a user.
 */
export const useUserListHandlers = (
  setMode: Dispatch<SetStateAction<string>>,
  setSelectedUser: Dispatch<SetStateAction<UserNamespace.User | null>>,
  setShowDel: Dispatch<SetStateAction<boolean>>,
  setPage: Dispatch<SetStateAction<number>>,
  fetchUsers: (page: number) => void,
) => {
  /**
   * Handles page change action.
   *
   * @param event - The event object.
   * @param newPage - The new page number to be set.
   */
  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
    fetchUsers(newPage + 1);
  };

  /**
   * Handles selecting a user and setting the appropriate mode.
   *
   * @param newMode - The new mode to be set.
   * @param newSelectUser - The user to be selected.
   */
  const handleSelectUser = (
    newMode: string,
    newSelectUser: UserNamespace.User | null,
  ) => {
    setMode(newMode);
    if (newMode === 'add') {
      const newUser: UserNamespace.User = {
        id: 0,
        name: 'New User',
        avatar: '',
        username: '',
        email: '',
        phone: '',
        website: '',
        company: '',
        dateJoined: '',
      };
      setSelectedUser(newUser);
    } else if (newMode === 'delete') {
      setSelectedUser(newSelectUser);
      setShowDel(true);
    } else {
      setSelectedUser(newSelectUser);
    }
  };

  return {
    handleChangePage,
    handleSelectUser,
  };
};
