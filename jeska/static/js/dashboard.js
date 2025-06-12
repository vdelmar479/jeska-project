document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
        new bootstrap.Tooltip(tooltipTriggerEl, {delay: { "show": 500, "hide": 100 }})
    );

    // Initialize Reports Chart
    let reportsChart = null;
    let devicesChart = null;

    function initReportsChart(data) {
        const options = {
            series: [{
                name: 'Reports',
                data: data.map(item => item.count)
            }],
            chart: {
                type: 'area',
                height: 350,
                toolbar: {
                    show: false
                },
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth',
                width: 3,
                colors: ['#ff914d']
            },
            markers: {
                size: 4,
                colors: ['#ff914d'],
                strokeColors: '#fff',
                strokeWidth: 2,
                hover: {
                    size: 7,
                    sizeOffset: 3
                }
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.7,
                    opacityTo: 0.3,
                    stops: [0, 90, 100],
                    colorStops: [
                        {
                            offset: 0,
                            color: '#ff914d',
                            opacity: 0.4
                        },
                        {
                            offset: 100,
                            color: '#ff914d',
                            opacity: 0.1
                        }
                    ]
                }
            },
            xaxis: {
                categories: data.map(item => {
                    const date = new Date(item.date);
                    return date.toLocaleDateString('en-GB', {
                        day: '2-digit',
                        month: '2-digit'
                    });
                }),
                tooltip: {
                    enabled: false
                }
            },
            yaxis: {
                labels: {
                    formatter: function(val) {
                        return Math.floor(val);
                    }
                },
                min: 0
            },
            tooltip: {
                theme: 'light',
                marker: {
                    show: true,
                    fillColors: ['#ff914d']
                },
                y: {
                    formatter: function(val) {
                        return Math.floor(val) + ' reports';
                    }
                }
            }
        };

        if (reportsChart) {
            reportsChart.destroy();
        }
        reportsChart = new ApexCharts(document.querySelector("#reportsChart"), options);
        reportsChart.render();
    }

    function initDevicesChart(data) {
        const options = {
            series: data.map(item => item.count),
            labels: data.map(item => item.status),
            chart: {
                type: 'donut',
                height: 350
            },
            colors: ['#28a745', '#dc3545', '#ffc107'], // Green for Active, Red for Down, Yellow for In Stock
            legend: {
                position: 'bottom',
                horizontalAlign: 'center'
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '70%',
                        labels: {
                            show: true,
                            total: {
                                show: true,
                                label: 'Total Devices',
                                formatter: function(w) {
                                    return w.globals.seriesTotals.reduce((a, b) => a + b, 0);
                                }
                            }
                        }
                    }
                }
            },
            dataLabels: {
                enabled: true,
                formatter: function(val, opts) {
                    return opts.w.config.series[opts.seriesIndex];
                }
            },
            tooltip: {
                y: {
                    formatter: function(val) {
                        return val + ' devices';
                    }
                }
            },
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        height: 350
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }]
        };

        if (devicesChart) {
            devicesChart.destroy();
        }
        devicesChart = new ApexCharts(document.querySelector("#devicesChart"), options);
        devicesChart.render();
    }

    // Fetch reports data for the chart
    fetch('/api/reports_last_seven_days')
        .then(response => response.json())
        .then(data => {
            initReportsChart(data);
        })
        .catch(error => {
            console.error('Error fetching reports data:', error);
        });

    // Fetch devices data for the chart
    fetch('/api/devices_by_status')
        .then(response => response.json())
        .then(data => {
            initDevicesChart(data);
        })
        .catch(error => {
            console.error('Error fetching devices data:', error);
        });

    // Initialize DataTable for recent reports
    const recentReportsTable = $('#recentReportsTable').DataTable({
        searching: false,
        paging: false,
        info: false,
        order: [[3, 'desc']], // Sort by date column by default
        columns: [
            { data: 'id' },
            { data: 'device_name' },
            { data: 'title' },
            { 
                data: 'created_at',
                render: function(data) {
                    return new Date(data).toLocaleString('en-GB', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit'
                    }).replace(',', '');
                }
            },
            { data: 'author_username' },
            {
                data: null,
                render: function(data) {
                    const currentUser = $('body').data('current-user');
                    const isAdmin = $('body').data('is-admin');
                    const canEdit = isAdmin || data.author_username === currentUser;
                    
                    let buttons = `
                        <button type="button" class="btn btn-sm btn-primary view-report-btn" data-report-id="${data.id}" data-bs-toggle="tooltip" data-bs-title="View report">
                            <i class="bi bi-eye-fill"></i>
                        </button>
                    `;
                    
                    if (canEdit) {
                        buttons += `
                            <button type="button" class="btn btn-sm btn-primary edit-report-btn" data-report-id="${data.id}" data-bs-toggle="tooltip" data-bs-title="Edit report">
                                <i class="bi bi-pencil-fill"></i>
                            </button>
                        `;
                    }
                    
                    return buttons;
                }
            }
        ]
    });

    // View report modal handling
    const viewModal = new bootstrap.Modal(document.getElementById('viewReportModal'));

    // Function to handle view report button clicks
    function handleViewReportClick(reportId, row) {
        // Get data from the table row
        const title = row.find('td:eq(2)').text();
        const device = row.find('td:eq(1)').text();
        const date = row.find('td:eq(3)').text();
        const author = row.find('td:eq(4)').text();

        // Update modal with data
        $('#reportTitle').text(title);
        $('#reportDevice').text(device);
        $('#reportStatus').html('<span class="badge bg-danger">Open</span>');
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
                const body = temp.querySelector('#report-body').textContent;
                $('#reportBody').text(body);
                
                // Show the modal
                viewModal.show();
            })
            .catch(error => {
                console.error('Error fetching report:', error);
                alert('Error loading report details');
            });
    }

    // Event delegation for view report buttons
    $('#recentReportsTable').on('click', '.view-report-btn', function() {
        const reportId = $(this).data('report-id');
        const row = $(this).closest('tr');
        handleViewReportClick(reportId, $(row));
    });

    // Fetch and populate recent reports
    fetch('/api/recent_active_reports')
        .then(response => response.json())
        .then(data => {
            recentReportsTable.clear();
            recentReportsTable.rows.add(data).draw();
            
            // Reinitialize tooltips after table update
            const newTooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            const newTooltipList = [...newTooltipTriggerList].map(tooltipTriggerEl => 
                new bootstrap.Tooltip(tooltipTriggerEl, {delay: { "show": 500, "hide": 100 }})
            );
        })
        .catch(error => {
            console.error('Error fetching recent reports:', error);
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
    $('#recentReportsTable').on('click', '.edit-report-btn', function() {
        const reportId = $(this).data('report-id');
        currentReportId = reportId;
        const row = $(this).closest('tr');
        
        // Get data from the table row
        const title = row.find('td:eq(2)').text();
        const device = row.find('td:eq(1)').text();
        const status = row.find('td:eq(2) .badge').text().trim() || 'Open';

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
                const body = temp.querySelector('#report-body').textContent;
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
});
