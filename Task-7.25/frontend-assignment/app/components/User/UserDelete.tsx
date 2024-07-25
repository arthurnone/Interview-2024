import React, { useContext } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

import { UserNamespace } from '@/app/types/user';
import UserContext from '@/app/context/UserContext';

const UserDelete: React.FC<UserNamespace.UserDeleteProps> = ({
  open,
  setOpen,
}) => {
  const context = useContext(UserContext);

  if (!context) {
    throw new Error('UserList must be used within a UserProvider');
  }

  const { selectedUser, delUser } = context;

  const handleClose = () => {
    setOpen(false);
  };

  const handlerDelUser = () => {
    handleClose();
    if (selectedUser && selectedUser.id) {
      delUser(selectedUser.id);
    }
  };

  return (
    <React.Fragment>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Delete {selectedUser?.name}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Please confirm your choice by clicking
            <span className="error-color font-bold"> Delete</span> or cancel to
            keep the user.
          </DialogContentText>
          <div className="flex mt-2">
            <span className="font-bold w-20 pr-2">Name:</span>
            <span>{selectedUser?.name}</span>
          </div>
          <div className="flex mt-1">
            <span className="font-bold w-20 pr-2">Email:</span>
            <span>{selectedUser?.email}</span>
          </div>
          <DialogContentText className="text-xs mt-2">
            Note: Deleting this user will permanently remove all associated
            data.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} variant="contained" autoFocus>
            Cancel
          </Button>
          <Button
            onClick={handlerDelUser}
            variant="contained"
            color="error"
            autoFocus
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
};

export default UserDelete;
