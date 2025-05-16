$(document).ready(function() {

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl,{delay: { "show": 500, "hide": 100 }}))

    $('.table').DataTable({
        responsive: true,
        searching: true,
        paging: true,
        pageLength: 10,
        ordering: true,
        colReorder: false,
        stateSave: true,
        language: {
            search: "Search devices:",
            lengthMenu: "Show _MENU_ devices per page",
            info: "Showing _START_ to _END_ of _TOTAL_ devices",
            infoEmpty: "No devices available",
            infoFiltered: "(filtered from _MAX_ total devices)",
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
                // Make the Status column sortable but not searchable
                targets: 1,
                searchable: false
            }
        ],
        // Initial sort by name column
        order: [[0, 'asc']]
    });

    // Delete device modal handling
    let deleteForm = null;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteDeviceModal'));

    // When delete button is clicked, store the form and show modal
    $('.delete-device-btn').on('click', function(e) {
        e.preventDefault();
        deleteForm = $(this).closest('form');
        deleteModal.show();
    });

    // When confirm delete is clicked in modal
    $('#confirmDeleteDeviceBtn').on('click', function() {
        if (deleteForm) {
            deleteForm.submit();
        }
        deleteModal.hide();
    });
});
