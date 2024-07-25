'use client';
import UserList from './components/User/UserList';
import { UserProvider } from './context/UserContext';

export default function Home() {
  return (
    <div className="min-h-screen p-4 max-w-screen-xl mx-auto">
      <UserProvider>
        <UserList />
      </UserProvider>
    </div>
  );
}
