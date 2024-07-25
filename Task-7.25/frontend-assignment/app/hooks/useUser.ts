import { useState } from 'react';
import { UserNamespace } from '@/app/types/user';

export const useUser = () => {
  const [selectedUser, setSelectedUser] = useState<UserNamespace.User | null>(
    null,
  );
  const [users, setUsers] = useState<UserNamespace.User[]>([]);

  return {
    users,
    selectedUser,
    setSelectedUser,
    setUsers,
  };
};
