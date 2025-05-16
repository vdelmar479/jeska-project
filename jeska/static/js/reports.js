$(document).ready(function() {

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl,{delay: { "show": 500, "hide": 100 }}))

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
                alert('Error loading report details');
            });
    });

    // Edit report modal handling
    const editModal = new bootstrap.Modal(document.getElementById('editReportModal'));
    let currentReportId = null;

    // When edit button is clicked, fetch report data and show modal
    $('.edit-report-btn').on('click', function() {
        const reportId = $(this).data('report-id');
        currentReportId = reportId;
        const row = $(this).closest('tr');
        
        // Get data from the table row
        const title = row.find('td:eq(3)').text();
        const device = row.find('td:eq(1)').text();
        const status = row.find('td:eq(2) .badge').text().trim();

        // Set initial form values
        $('#editTitle').val(title);
        $('#editDeviceName').val(device);
        $('#editDeviceNameHidden').val(device);
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
                alert('Error loading report details');
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
            alert('Error updating report');
        });
    });
});
