import { UserNamespace } from './user';

export interface Column {
  id: keyof UserNamespace.User;
  label: string;
  required: boolean;
}

export const columns: Column[] = [
  { id: 'name', label: 'Name', required: true },
  { id: 'email', label: 'Email', required: true },
  { id: 'phone', label: 'Phone', required: false },
  { id: 'company', label: 'Company', required: false },
  { id: 'website', label: 'Website', required: false },
];
