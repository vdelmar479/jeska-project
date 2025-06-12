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
                <p>Creating report...</p>
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

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl,{delay: { "show": 500, "hide": 100 }}))

    // Initialize Select2 for device selects
    $('#createDeviceName').select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Select a device',
        allowClear: true,
        dropdownParent: $('#createReportModal'),
        minimumResultsForSearch: 0
    });

    $('#editDeviceName').select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Select a device',
        allowClear: true,
        dropdownParent: $('#editReportModal'),
        minimumResultsForSearch: 0
    });

    // Initialize DataTable
    var table = $('.table').DataTable({
        responsive: true,
        searching: true,
        paging: true,
        pageLength: 10,
        ordering: true,
        colReorder: false,
        stateSave: true,
        language: {
            search: "Search reports:",
            lengthMenu: "Show _MENU_ reports per page",
            info: "Showing _START_ to _END_ of _TOTAL_ reports",
            infoEmpty: "No reports available",
            infoFiltered: "(filtered from _MAX_ total reports)",
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
                // Make the Action column not sortable
                targets: -1,
                orderable: false,
                searchable: false
            },
            {
                // Make the Status column sortable but not searchable
                targets: 2,
                searchable: false
            }
        ],
        // Initial sort by date column (descending)
        order: [[4, 'desc']]
    });

    // Function to apply all filters
    function applyFilters() {
        var showClosed = $('#showClosedReports').is(':checked');
        var showOwn = $('#showOwnReports').is(':checked');
        
        // Clear any existing custom filters
        $.fn.dataTable.ext.search.pop();
        
        // Add new filter function
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var row = $(table.row(dataIndex).node());
                var status = row.find('td:eq(2) .badge').text().trim();
                var author = row.find('td:eq(5)').text().trim();
                var currentUser = $('body').data('current-user');
                
                // Check closed reports filter
                if (!showClosed && status === 'Closed') {
                    return false;
                }
                
                // Check own reports filter
                if (showOwn && author !== currentUser) {
                    return false;
                }
                
                return true;
            }
        );
        
        table.draw();
    }

    // Initial filter
    applyFilters();

    // Handle checkbox changes
    $('#showClosedReports, #showOwnReports').on('change', function() {
        applyFilters();
    });

    // Delete report modal handling
    let deleteForm = null;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteReportModal'));

    // When delete button is clicked, store the form and show modal
    $('.delete-report-btn').on('click', function(e) {
        e.preventDefault();
        deleteForm = $(this).closest('form');
        deleteModal.show();
    });

    // When confirm delete is clicked in modal
    $('#confirmDeleteBtn').on('click', function() {
        if (deleteForm) {
            deleteForm.submit();
        }
        deleteModal.hide();
    });

    // View report modal handling
    const viewModal = new bootstrap.Modal(document.getElementById('viewReportModal'));

    // When view button is clicked, fetch report data and show modal
    $('.view-report-btn').on('click', function() {
        const reportId = $(this).data('report-id');
        const row = $(this).closest('tr');
        
        // Get data from the table row
        const title = row.find('td:eq(3)').text();
        const device = row.find('td:eq(1)').text();
        const status = row.find('td:eq(2) .badge').text().trim();
        const date = row.find('td:eq(4)').text();
        const author = row.find('td:eq(5)').text();

        // Update modal with data
        $('#reportTitle').text(title);
        $('#reportDevice').text(device);
        $('#reportStatus').html(`<span class="badge ${status === 'Open' ? 'bg-danger' : status === 'In Progress' ? 'bg-warning' : 'bg-success'}">${status}</span>`);
        $('#reportAuthor').text(author);
        $('#reportDate').text(date);

        // Get device ID and update the view device link
        fetch(`/api/device_id_by_name/${encodeURIComponent(device)}`)
            .then(response => response.json())
            .then(data => {
                const viewDeviceLink = document.querySelector('#viewReportModal .action.btn.btn-secondary');
                viewDeviceLink.href = `/devices/${data.id}/view`;
                viewDeviceLink.target = '_blank';
            })
            .catch(error => {
                console.error('Error fetching device ID:', error);
            });

        // Fetch report body from the server
        fetch(`/reports/${reportId}/view`)
            .then(response => response.text())
            .then(html => {
                // Create a temporary element to parse the HTML
                const temp = document.createElement('div');
                temp.innerHTML = html;
                
                // Extract the report body from the response
                const body = $(temp).find('#report-body').text();
                $('#reportBody').text(body);
                
                // Show the modal
                viewModal.show();
            })
            .catch(error => {
                console.error('Error fetching report:', error);
                showAlert('Error loading report details');
            });
    });

    // Edit report modal handling
    const editModal = new bootstrap.Modal(document.getElementById('editReportModal'));
    let currentReportId = null;
    let deviceNames = []; // Store device names

    // Fetch device names when page loads
    fetch('/api/list_devices_names')
        .then(response => response.json())
        .then(names => {
            deviceNames = names;
        })
        .catch(error => {
            console.error('Error fetching device names:', error);
        });

    // When edit button is clicked, fetch report data and show modal
    $('.edit-report-btn').on('click', function() {
        const reportId = $(this).data('report-id');
        currentReportId = reportId;
        const row = $(this).closest('tr');
        
        // Get data from the table row
        const title = row.find('td:eq(3)').text();
        const device = row.find('td:eq(1)').text();
        const status = row.find('td:eq(2) .badge').text().trim();

        // Populate device select options
        const deviceSelect = $('#editDeviceName');
        deviceSelect.empty();
        deviceNames.forEach(name => {
            deviceSelect.append($('<option>', {
                value: name,
                text: name,
                selected: name === device
            }));
        });

        // Set initial form values
        $('#editTitle').val(title);
        $('#editStatus').val(status);

        // Fetch report body from the server
        fetch(`/reports/${reportId}/view`)
            .then(response => response.text())
            .then(html => {
                // Create a temporary element to parse the HTML
                const temp = document.createElement('div');
                temp.innerHTML = html;
                
                // Extract the report body from the response
                const body = $(temp).find('#report-body').text();
                $('#editBody').val(body);
                
                // Show the modal
                editModal.show();
            })
            .catch(error => {
                console.error('Error fetching report:', error);
                showAlert('Error loading report details');
            });
    });

    // Handle form submission
    $('#saveReportBtn').on('click', function() {
        if (!currentReportId) return;

        const formData = new FormData(document.getElementById('editReportForm'));
        
        // Send POST request to update the report
        fetch(`/reports/${currentReportId}/update`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Reload the page to show updated data
            window.location.reload();
        })
        .catch(error => {
            console.error('Error updating report:', error);
            showAlert('Error updating report');
        });
    });

    // Create report modal handling
    const createReportModal = new bootstrap.Modal(document.getElementById('createReportModal'));

    // When new report button is clicked
    $('#newReportBtn').on('click', function() {
        // Reset form
        $('#createTitle').val('');
        $('#createDeviceName').val('');
        $('#createBody').val('');
        createReportModal.show();
    });

    // When save new report button is clicked
    $('#saveNewReportBtn').on('click', function() {
        const data = {
            title: $('#createTitle').val(),
            device_name: $('#createDeviceName').val(),
            status: 'Open', // Always set to Open for new reports
            body: $('#createBody').val()
        };

        // Validate required fields
        if (!data.title || !data.device_name) {
            showAlert('Title and Device are required fields.');
            return;
        }

        // Show loading overlay
        $('#loadingOverlay').show();

        fetch('/api/report', {
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
            // Hide loading overlay
            $('#loadingOverlay').hide();
            createReportModal.hide();
            // Reload the page to show the new report
            window.location.reload();
        })
        .catch(error => {
            // Hide loading overlay
            $('#loadingOverlay').hide();
            console.error('Error:', error);
            showAlert('Error creating report. Please try again.');
        });
    });
});
