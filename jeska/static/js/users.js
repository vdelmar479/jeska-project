$(document).ready(function() {

    // Add alert container if it doesn't exist
    if (!$('#alertContainer').length) {
        $('body').prepend('<div id="alertContainer" style="position: fixed; top: 20px; right: 20px; z-index: 9999;"></div>');
    }

    // Function to show Bootstrap alert
    function showAlert(message, type = 'danger') {
        const alertId = 'alert-' + Date.now();
        const alertHtml = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        $('#alertContainer').append(alertHtml);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            $(`#${alertId}`).alert('close');
        }, 5000);
    }

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl,{delay: { "show": 500, "hide": 100 }}))

    // Initialize modals only if they exist
    const editProfileModalEl = document.getElementById('editProfileModal');
    const changePasswordModalEl = document.getElementById('changePasswordModal');
    const editUserModalEl = document.getElementById('editUserModal');
    const deleteUserModalEl = document.getElementById('deleteUserModal');
    const resetPasswordModalEl = document.getElementById('resetPasswordModal');

    const editProfileModal = editProfileModalEl ? new bootstrap.Modal(editProfileModalEl) : null;
    const changePasswordModal = changePasswordModalEl ? new bootstrap.Modal(changePasswordModalEl) : null;
    const editUserModal = editUserModalEl ? new bootstrap.Modal(editUserModalEl) : null;
    const deleteUserModal = deleteUserModalEl ? new bootstrap.Modal(deleteUserModalEl) : null;
    const resetPasswordModal = resetPasswordModalEl ? new bootstrap.Modal(resetPasswordModalEl) : null;

    // Show edit profile modal
    if (editProfileModal) {
        $('#editProfileBtn').on('click', function() {
            editProfileModal.show();
        });
    }

    // Show change password modal
    if (changePasswordModal) {
        $('#changePasswordBtn').on('click', function() {
            changePasswordModal.show();
        });
    }

    // Show edit user modal and populate fields
    if (editUserModal) {
        $('.edit-user-btn').on('click', function() {
            const userId = $(this).data('user-id');
            const username = $(this).data('username');
            const name = $(this).data('name');
            const surname = $(this).data('surname');
            const email = $(this).data('email');
            const role = $(this).data('role');

            $('#editUserId').val(userId);
            $('#editUsername').val(username);
            $('#editName').val(name);
            $('#editSurname').val(surname);
            $('#editEmail').val(email);
            $('#editRole').val(role);

            editUserModal.show();
        });
    }

    // Delete user modal handling
    if (deleteUserModal) {
        let currentDeleteForm = null;

        // Show delete modal and store the form
        $('.delete-user-btn').on('click', function() {
            const userId = $(this).data('user-id');
            const username = $(this).data('username');
            
            currentDeleteForm = $(`#deleteForm${userId}`);
            $('#deleteUserName').text(username);
            
            deleteUserModal.show();
        });

        // Handle delete confirmation
        $('#confirmDeleteBtn').on('click', function() {
            if (currentDeleteForm) {
                currentDeleteForm.submit();
            }
            deleteUserModal.hide();
        });
    }

    // Handle profile update
    if (editProfileModal) {
        $('#saveProfileBtn').on('click', function() {
            const data = {
                name: $('#editName').val(),
                surname: $('#editSurname').val(),
                email: $('#editEmail').val()
            };

            fetch('/api/update_profile', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                editProfileModal.hide();
                // Reload the page to show updated data
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error updating profile. Please try again.');
            });
        });
    }

    // Handle user update
    if (editUserModal) {
        $('#saveUserBtn').on('click', function() {
            const userId = $('#editUserId').val();
            const data = {
                name: $('#editName').val(),
                surname: $('#editSurname').val(),
                email: $('#editEmail').val(),
                role: $('#editRole').val()
            };

            fetch(`/api/update_user/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 403) {
                        throw new Error('You do not have permission to update users');
                    }
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                editUserModal.hide();
                // Reload the page to show updated data
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert(error.message || 'Error updating user. Please try again.');
            });
        });
    }

    // Handle password change
    if (changePasswordModal) {
        $('#savePasswordBtn').on('click', function() {
            const newPassword = $('#newPassword').val();
            const confirmPassword = $('#confirmPassword').val();

            if (newPassword !== confirmPassword) {
                showAlert('New passwords do not match');
                return;
            }

            const data = {
                current_password: $('#currentPassword').val(),
                new_password: newPassword
            };

            fetch('/api/change_password', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('Current password is incorrect');
                    }
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                changePasswordModal.hide();
                showAlert('Password changed successfully', 'success');
                // Clear the form
                $('#changePasswordForm')[0].reset();
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert(error.message || 'Error changing password. Please try again.');
            });
        });
    }

    // Show reset password modal
    if (resetPasswordModal) {
        $('.reset-password-btn').on('click', function() {
            const userId = $(this).data('user-id');
            const username = $(this).data('username');
            
            $('#resetPasswordUserId').val(userId);
            $('#resetPasswordUsername').text(username);
            $('#resetPasswordForm')[0].reset();
            $('#resetPasswordError').hide();
            
            resetPasswordModal.show();
        });

        // Handle reset password
        $('#saveResetPasswordBtn').on('click', function() {
            const newPassword = $('#resetNewPassword').val();
            const confirmPassword = $('#resetConfirmPassword').val();
            const userId = $('#resetPasswordUserId').val();

            if (newPassword !== confirmPassword) {
                $('#resetPasswordError').text('New passwords do not match').show();
                return;
            }

            const data = {
                new_password: newPassword
            };

            fetch(`/auth/api/reset_password/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 403) {
                        throw new Error('You do not have permission to reset passwords');
                    }
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resetPasswordModal.hide();
                showAlert('Password reset successfully', 'success');
                // Clear the form
                $('#resetPasswordForm')[0].reset();
            })
            .catch(error => {
                console.error('Error:', error);
                $('#resetPasswordError').text(error.message || 'Error resetting password. Please try again.').show();
            });
        });
    }

    // Initialize DataTable if there's a table present
    if ($('.table').length) {
        $('.table').DataTable({
            responsive: true,
            searching: true,
            paging: true,
            pageLength: 10,
            ordering: true,
            colReorder: false,
            stateSave: true,
            language: {
                search: "Search users:",
                lengthMenu: "Show _MENU_ users per page",
                info: "Showing _START_ to _END_ of _TOTAL_ users",
                infoEmpty: "No users available",
                infoFiltered: "(filtered from _MAX_ total users)",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "Next",
                    previous: "Previous"
                }
            },
            // Column specific configurations
            columnDefs: [
                {
                    // Make the Actions column not sortable
                    targets: -1,
                    orderable: false,
                    searchable: false
                },
                {
                    // Make the Role column sortable but not searchable
                    targets: 5,
                    searchable: false
                }
            ],
            // Initial sort by username column
            order: [[1, 'asc']]
        });
    }

    // Show new user modal
    $('#newUserBtn').on('click', function() {
        $('#newUserForm')[0].reset();
        $('#newUserError').hide();
        const newUserModal = new bootstrap.Modal(document.getElementById('newUserModal'));
        newUserModal.show();
    });

    // Handle new user registration
    $('#saveNewUserBtn').on('click', function() {
        const data = {
            username: $('#newUsername').val(),
            password: $('#newPassword').val(),
            name: $('#newName').val(),
            surname: $('#newSurname').val(),
            email: $('#newEmail').val(),
            role: $('#newRole').val()
        };
        $.ajax({
            url: '/auth/register',
            type: 'POST',
            data: data,
            success: function(response) {
                if (response.ok) {
                    const newUserModal = bootstrap.Modal.getInstance(document.getElementById('newUserModal'));
                    newUserModal.hide();
                    window.location.reload();
                } else {
                    $('#newUserError').text(response.error || 'Registration failed.').show();
                }
            },
            error: function(xhr) {
                let errorMsg = 'Registration failed.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                $('#newUserError').text(errorMsg).show();
            }
        });
    });
});
