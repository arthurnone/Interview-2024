export declare namespace UserNamespace {
  export interface User {
    id: number | null;
    name: string;
    username: string;
    avatar: string;
    email: string;
    phone: string;
    website: string;
    company: string;
    dateJoined: string;
  }

  export interface UserContextProps {
    users: User[];
    selectedUser: User | null;
    setSelectedUser: (user: User | null) => void;
    setUsers: (users: User[]) => void;
    fetchUsers: (page: number) => void;
    addUser: (users: User) => void;
    updateUser: (users: User) => void;
    delUser: (id: number) => void;
  }

  export interface UserDeleteProps {
    open: boolean;
    setOpen: (open: boolean) => void;
  }

  export interface UserDetailProps {
    mode: string;
  }
}
