import React, { useContext } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Skeleton from '@mui/material/Skeleton';

import { UserNamespace } from '@/app/types/user';
import { useColumns } from '@/app/hooks/useColumns';
import UserContext from '@/app/context/UserContext';

const UserDetail: React.FC<UserNamespace.UserDetailProps> = ({ mode }) => {
  const context = useContext(UserContext);

  if (!context) {
    throw new Error('UserList must be used within a UserProvider');
  }

  const { selectedUser, setSelectedUser, addUser, updateUser } = context;
  const columns = useColumns();

  const handleClose = () => {
    setSelectedUser(null);
  };

  const handleAddUser = () => {
    if (!checkForm()) {
      return;
    }
    handleClose();
    if (selectedUser) {
      addUser(selectedUser);
    }
  };

  const handleUpdateUser = () => {
    if (!checkForm()) {
      return;
    }
    handleClose();
    if (selectedUser) {
      updateUser(selectedUser);
    }
  };

  const checkForm = (): boolean => {
    if (checkError('username')) {
      return false;
    }
    for (const col of columns) {
      if (checkError(col.id)) {
        return false;
      }
    }
    return true;
  };

  const checkError = (label: string): boolean => {
    if (label === 'username' && !selectedUser?.username) {
      return true;
    }
    for (const col of columns) {
      if (col.id === label && col.required && !selectedUser?.[col.id]) {
        return true;
      }
    }
    return false;
  };

  if (!selectedUser) {
    return null;
  }

  const handleChange = (key: keyof UserNamespace.User, value: string) => {
    setSelectedUser({
      ...selectedUser,
      [key]: value,
    });
  };

  return (
    <React.Fragment>
      <Dialog
        open={selectedUser !== null}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {mode === 'add' ? 'Add New User' : `${selectedUser?.name}'s Detail`}
        </DialogTitle>
        <DialogContent>
          <Box
            component="form"
            sx={{
              '& .MuiTextField-root': { m: 1, width: '25ch' },
            }}
            noValidate
            autoComplete="off"
          >
            <div className="flex flex-col md:flex-row items-center">
              <div className="w-full md:w-1/2 flex justify-center mb-4 md:mb-0">
                {selectedUser.avatar ? (
                  <img
                    src={selectedUser?.avatar}
                    alt="img"
                    width="128"
                    height="128"
                    loading="lazy"
                    className="object-cover m-auto"
                  />
                ) : (
                  <Skeleton variant="rectangular" width={128} height={128} />
                )}
              </div>
              <div className="w-full md:w-1/2 mr-0 md:mr-5">
                <TextField
                  label="ID"
                  value={selectedUser?.id}
                  fullWidth
                  disabled
                />
                <TextField
                  error={checkError('username')}
                  required
                  InputProps={{
                    readOnly: mode !== 'edit' && mode !== 'add',
                  }}
                  id="outlined-required"
                  label="Username"
                  value={selectedUser?.username}
                  onChange={e => handleChange('username', e.target.value)}
                  fullWidth
                />
              </div>
            </div>
            <div>
              {columns.map(col => (
                <TextField
                  error={checkError(col.id)}
                  required={col.required}
                  InputProps={{
                    readOnly: mode !== 'edit' && mode !== 'add',
                  }}
                  label={col.label}
                  value={selectedUser[col.id]}
                  onChange={e => handleChange(col.id, e.target.value)}
                  fullWidth
                  key={col.id}
                />
              ))}
              <TextField
                disabled
                label="Date Joined"
                value={selectedUser?.dateJoined}
                fullWidth
              />
            </div>
          </Box>
          <DialogContentText id="alert-dialog-description"></DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
          {mode === 'add' && (
            <Button onClick={handleAddUser} variant="contained" color="success">
              Add
            </Button>
          )}
          {mode === 'edit' && (
            <Button
              onClick={handleUpdateUser}
              variant="contained"
              color="success"
            >
              Submit
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
};

export default UserDetail;
