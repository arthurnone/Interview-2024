import React, { useEffect, useContext } from 'react';
import Avatar from '@mui/material/Avatar';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

import { useColumns } from '@/app/hooks/useColumns';
import UserContext from '@/app/context/UserContext';
import { useUserListHandlers } from '@/app/handlers/userListHandlers';

import UserDetail from './UserDetail';
import UserDelete from './UserDelete';

const UserList: React.FC = () => {
  const context = useContext(UserContext);

  if (!context) {
    throw new Error('UserList must be used within a UserProvider');
  }

  const { users, selectedUser, setSelectedUser, fetchUsers } = context;
  const [mode, setMode] = React.useState<string>('read');
  const [showDel, setShowDel] = React.useState<boolean>(false);
  const [page, setPage] = React.useState(0);
  const columns = useColumns();

  const { handleChangePage, handleSelectUser } = useUserListHandlers(
    setMode,
    setSelectedUser,
    setShowDel,
    setPage,
    fetchUsers,
  );

  useEffect(() => {
    fetchUsers(1);
  }, [fetchUsers]);

  return (
    <React.Fragment>
      <Button
        variant="outlined"
        color="success"
        onClick={() => handleSelectUser('add', null)}
        className="mb-5"
      >
        <AddIcon />
        Add User
      </Button>

      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        {selectedUser && mode !== 'delete' && <UserDetail mode={mode} />}
        {selectedUser && mode === 'delete' && (
          <UserDelete open={showDel} setOpen={setShowDel} />
        )}

        <TableContainer sx={{ minHeight: 440 }}>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }}>
              <TableHead>
                <TableRow>
                  <TableCell align="left">ID</TableCell>
                  <TableCell align="left">Avatar</TableCell>
                  <TableCell align="right">Username</TableCell>
                  {columns.map(col => (
                    <TableCell key={col.label} align="right">
                      {col.label}
                    </TableCell>
                  ))}
                  <TableCell align="center">Edit</TableCell>
                  <TableCell align="center">Delete</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {users.map(user => (
                  <TableRow
                    key={user.name}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell>{user.id}</TableCell>
                    <TableCell>
                      <Avatar alt={user.name} src={user.avatar} />
                    </TableCell>
                    <TableCell
                      onClick={() => handleSelectUser('read', user)}
                      align="right"
                    >
                      <Button variant="text">{user.username}</Button>
                    </TableCell>
                    {columns.map(col => (
                      <TableCell align="right" key={col.id}>
                        {user[col.id]}
                      </TableCell>
                    ))}
                    <TableCell align="center">
                      <Button
                        variant="outlined"
                        size="small"
                        color="success"
                        onClick={() => handleSelectUser('edit', user)}
                      >
                        <EditIcon className="h-4 w-4 mr-1" />
                        Edit
                      </Button>
                    </TableCell>
                    <TableCell align="center">
                      <Button
                        variant="outlined"
                        size="small"
                        color="error"
                        onClick={() => handleSelectUser('delete', user)}
                      >
                        <DeleteIcon className="h-4 w-4 mr-1" />
                        Delete
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[10]}
          component="div"
          count={100}
          rowsPerPage={10}
          page={page}
          onPageChange={handleChangePage}
        />
      </Paper>
    </React.Fragment>
  );
};

export default UserList;
