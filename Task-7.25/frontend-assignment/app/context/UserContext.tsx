import React, { createContext, ReactNode, useCallback } from 'react';

import { UserNamespace } from '@/app/types/user';
import { useUser } from '@/app/hooks/useUser';
import { useUserActions } from '@/app/hooks/useUserActions';

const UserContext = createContext<UserNamespace.UserContextProps | undefined>(
  undefined,
);

export const UserProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const { users, selectedUser, setSelectedUser, setUsers } = useUser();
  const { fetchUsers, addUser, updateUser, delUser } = useUserActions(setUsers);

  return (
    <UserContext.Provider
      value={{
        users,
        selectedUser,
        setSelectedUser,
        setUsers,
        fetchUsers,
        addUser,
        updateUser,
        delUser,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};

export default UserContext;
