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

    // Add loading overlay HTML
    $('body').append(`
        <div id="loadingOverlay" style="display: none;">
            <div class="loading-content">
                <img src="/static/img/loading.gif" alt="Loading..." />
                <p>Consolidating peripherals...</p>
            </div>
        </div>
    `);

    // Add CSS for loading overlay
    $('head').append(`
        <style>
            #loadingOverlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 9999;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .loading-content {
                background: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }
            .loading-content img {
                width: 50px;
                height: 50px;
                margin-bottom: 10px;
            }
            .loading-content p {
                margin: 0;
                color: #666;
            }
        </style>
    `);

    // Initialize DataTable
    $('.table').DataTable({
        responsive: true,
        searching: true,
        paging: true,
        pageLength: 10,
        ordering: true,
        colReorder: false,
        stateSave: true,
        language: {
            search: "Search peripherals:",
            lengthMenu: "Show _MENU_ peripherals per page",
            info: "Showing _START_ to _END_ of _TOTAL_ peripherals",
            infoEmpty: "No peripherals available",
            infoFiltered: "(filtered from _MAX_ total peripherals)",
            paginate: {
                first: "First",
                last: "Last",
                next: "Next",
                previous: "Previous"
            }
        },
        columnDefs: [
            {
                targets: -1,
                orderable: false,
                searchable: false
            }
        ],
        order: [[0, 'asc']]
    });

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl, {
        delay: { "show": 500, "hide": 100 }
    }));

    // Modal instances
    const createPeripheralModal = new bootstrap.Modal(document.getElementById('createPeripheralModal'));
    const editPeripheralModal = new bootstrap.Modal(document.getElementById('editPeripheralModal'));
    const deletePeripheralModal = new bootstrap.Modal(document.getElementById('deletePeripheralModal'));
    const viewPeripheralModal = new bootstrap.Modal(document.getElementById('viewPeripheralModal'));

    // Create peripheral handling
    $('#newPeripheralBtn').on('click', function() {
        // Reset form
        $('#createPeripheralName').val('');
        $('#createPeripheralType').val('');
        $('#createPeripheralDescription').val('');
        $('#createPeripheralTotal').val(0);
        createPeripheralModal.show();
    });

    // Save new peripheral
    $('#saveNewPeripheralBtn').on('click', function() {
        const data = {
            name: $('#createPeripheralName').val(),
            type: $('#createPeripheralType').val(),
            description: $('#createPeripheralDescription').val(),
            total: parseInt($('#createPeripheralTotal').val())
        };

        // Validate required fields
        if (!data.name || !data.type) {
            showAlert('Name and Type are required fields.');
            return;
        }

        fetch('/peripherals/api/peripheral', {
            method: 'POST',
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
            createPeripheralModal.hide();
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error creating peripheral. Please try again.');
        });
    });

    // Edit peripheral handling
    $('.edit-peripheral-btn').on('click', function() {
        const button = $(this);
        const peripheralId = button.data('peripheral-id');
        const peripheralName = button.data('peripheral-name');
        const peripheralType = button.data('peripheral-type');
        const peripheralDescription = button.data('peripheral-description');
        const peripheralTotal = button.data('peripheral-total');

        $('#editPeripheralId').val(peripheralId);
        $('#editPeripheralName').val(peripheralName);
        $('#editPeripheralType').val(peripheralType);
        $('#editPeripheralDescription').val(peripheralDescription);
        $('#editPeripheralTotal').val(peripheralTotal);

        editPeripheralModal.show();
    });

    // Save edited peripheral
    $('#savePeripheralBtn').on('click', function() {
        const peripheralId = $('#editPeripheralId').val();
        const data = {
            name: $('#editPeripheralName').val(),
            type: $('#editPeripheralType').val(),
            description: $('#editPeripheralDescription').val(),
            total: parseInt($('#editPeripheralTotal').val())
        };

        // Validate required fields
        if (!data.name || !data.type) {
            showAlert('Name and Type are required fields.');
            return;
        }

        fetch(`/peripherals/api/peripheral/${peripheralId}`, {
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
            const row = $(`button[data-peripheral-id="${peripheralId}"]`).closest('tr');
            row.find('td:eq(0)').text(data.name);
            row.find('td:eq(1)').text(data.type);
            row.find('td:eq(2)').text(data.description || 'N/A');
            row.find('td:eq(3)').text(data.in_use);
            row.find('td:eq(4)').text(data.total);
            row.find('td:eq(5)').text(data.total - data.in_use);

            // Update edit button data attributes
            const editBtn = row.find('.edit-peripheral-btn');
            editBtn.data('peripheral-name', data.name);
            editBtn.data('peripheral-type', data.type);
            editBtn.data('peripheral-description', data.description);
            editBtn.data('peripheral-total', data.total);

            editPeripheralModal.hide();
            showAlert('Peripheral updated successfully!', 'success');
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error updating peripheral. Please try again.');
        });
    });

    // Delete peripheral handling
    let deleteForm = null;
    $('.delete-peripheral-btn').on('click', function(e) {
        e.preventDefault();
        const peripheralId = $(this).data('peripheral-id');
        deleteForm = $(`#deleteForm${peripheralId}`);
        deletePeripheralModal.show();
    });

    $('#confirmDeletePeripheralBtn').on('click', function() {
        if (deleteForm) {
            deleteForm.submit();
        }
        deletePeripheralModal.hide();
    });

    // View peripheral handling
    $('.view-peripheral-btn').on('click', function() {
        const peripheralId = $(this).data('peripheral-id');

        fetch(`/peripherals/api/peripheral/${peripheralId}`)
            .then(response => response.json())
            .then(peripheral => {
                $('#peripheralName').text(peripheral.name);
                $('#peripheralType').text(peripheral.type);
                $('#peripheralDescription').text(peripheral.description || 'N/A');
                $('#peripheralInUse').text(peripheral.in_use);
                $('#peripheralTotal').text(peripheral.total);
                $('#peripheralAvailable').text(peripheral.total - peripheral.in_use);
                viewPeripheralModal.show();
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error loading peripheral details. Please try again.');
            });
    });

    // Consolidate peripherals handling
    $('#consolidatePeripheralBtn').on('click', function() {
        // Show loading overlay
        $('#loadingOverlay').show();

        fetch('/peripherals/consolidate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading overlay
            $('#loadingOverlay').hide();
            
            // Create alert HTML
            const alertHtml = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Success!</strong> ${data.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            
            // Insert alert at the top of the page
            $('.container').prepend(alertHtml);
            
            // Reload the page after 2 seconds to show updated data
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        })
        .catch(error => {
            // Hide loading overlay
            $('#loadingOverlay').hide();
            
            console.error('Error:', error);
            const alertHtml = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Error!</strong> Failed to consolidate peripherals. Please try again.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            $('.container').prepend(alertHtml);
        });
    });
});
