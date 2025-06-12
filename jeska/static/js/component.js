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
                <p>Consolidating components...</p>
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
            search: "Search components:",
            lengthMenu: "Show _MENU_ components per page",
            info: "Showing _START_ to _END_ of _TOTAL_ components",
            infoEmpty: "No components available",
            infoFiltered: "(filtered from _MAX_ total components)",
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
    const createComponentModal = new bootstrap.Modal(document.getElementById('createComponentModal'));
    const editComponentModal = new bootstrap.Modal(document.getElementById('editComponentModal'));
    const deleteComponentModal = new bootstrap.Modal(document.getElementById('deleteComponentModal'));
    const viewComponentModal = new bootstrap.Modal(document.getElementById('viewComponentModal'));

    // Create component handling
    $('#newComponentBtn').on('click', function() {
        // Reset form
        $('#createComponentName').val('');
        $('#createComponentType').val('');
        $('#createComponentDescription').val('');
        $('#createComponentTotal').val(0);
        createComponentModal.show();
    });

    // Save new component
    $('#saveNewComponentBtn').on('click', function() {
        const data = {
            name: $('#createComponentName').val(),
            type: $('#createComponentType').val(),
            description: $('#createComponentDescription').val(),
            total: parseInt($('#createComponentTotal').val())
        };

        // Validate required fields
        if (!data.name || !data.type) {
            showAlert('Name and Type are required fields.');
            return;
        }

        fetch('/api/component', {
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
            createComponentModal.hide();
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error creating component. Please try again.');
        });
    });

    // Edit component handling
    $('.edit-component-btn').on('click', function() {
        const button = $(this);
        const componentId = button.data('component-id');
        const componentName = button.data('component-name');
        const componentType = button.data('component-type');
        const componentDescription = button.data('component-description');
        const componentTotal = button.data('component-total');

        $('#editComponentId').val(componentId);
        $('#editComponentName').val(componentName);
        $('#editComponentType').val(componentType);
        $('#editComponentDescription').val(componentDescription);
        $('#editComponentTotal').val(componentTotal);

        editComponentModal.show();
    });

    // Save edited component
    $('#saveComponentBtn').on('click', function() {
        const componentId = $('#editComponentId').val();
        const data = {
            name: $('#editComponentName').val(),
            type: $('#editComponentType').val(),
            description: $('#editComponentDescription').val(),
            total: parseInt($('#editComponentTotal').val())
        };

        // Validate required fields
        if (!data.name || !data.type) {
            showAlert('Name and Type are required fields.');
            return;
        }

        fetch(`/api/component/${componentId}`, {
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
            const row = $(`button[data-component-id="${componentId}"]`).closest('tr');
            row.find('td:eq(0)').text(data.name);
            row.find('td:eq(1)').text(data.type);
            row.find('td:eq(2)').text(data.description || 'N/A');
            row.find('td:eq(3)').text(data.in_use);
            row.find('td:eq(4)').text(data.total);
            row.find('td:eq(5)').text(data.total - data.in_use);

            // Update edit button data attributes
            const editBtn = row.find('.edit-component-btn');
            editBtn.data('component-name', data.name);
            editBtn.data('component-type', data.type);
            editBtn.data('component-description', data.description);
            editBtn.data('component-total', data.total);

            editComponentModal.hide();
            showAlert('Component updated successfully!', 'success');
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error updating component. Please try again.');
        });
    });

    // Delete component handling
    let deleteForm = null;
    $('.delete-component-btn').on('click', function(e) {
        e.preventDefault();
        const componentId = $(this).data('component-id');
        deleteForm = $(`#deleteForm${componentId}`);
        deleteComponentModal.show();
    });

    $('#confirmDeleteComponentBtn').on('click', function() {
        if (deleteForm) {
            deleteForm.submit();
        }
        deleteComponentModal.hide();
    });

    // View component handling
    $('.view-component-btn').on('click', function() {
        const componentId = $(this).data('component-id');

        fetch(`/api/component/${componentId}`)
            .then(response => response.json())
            .then(component => {
                $('#componentName').text(component.name);
                $('#componentType').text(component.type);
                $('#componentDescription').text(component.description || 'N/A');
                $('#componentInUse').text(component.in_use);
                $('#componentTotal').text(component.total);
                $('#componentAvailable').text(component.total - component.in_use);
                viewComponentModal.show();
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error loading component details. Please try again.');
            });
    });

    // Consolidate components handling
    $('#consolidateComponentBtn').on('click', function() {
        // Show loading overlay
        $('#loadingOverlay').show();

        fetch('/components/consolidate', {
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
                    <strong>Error!</strong> Failed to consolidate components. Please try again.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            $('.container').prepend(alertHtml);
        });
    });
});
