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
});
