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

    $('.table').not('#deviceActiveReports .table').DataTable({
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

    // Create device modal handling
    const createDeviceModal = new bootstrap.Modal(document.getElementById('createDeviceModal'));

    // Initialize Select2 for components
    $('#createDeviceComponents').select2({
        theme: 'bootstrap-5',
        width: '100%',
        ajax: {
            url: '/api/list_component_names',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    search: params.term, // search term
                    page: params.page
                };
            },
            processResults: function (data, params) {
                // Filter results based on search term
                const term = (params.term || '').toLowerCase();
                const filtered = data.filter(name => 
                    name.toLowerCase().includes(term)
                );
                
                return {
                    results: filtered.map(name => ({
                        id: name,
                        text: name
                    }))
                };
            },
            cache: true
        },
        placeholder: 'Select components',
        allowClear: true,
        tags: true,
        multiple: true,
        minimumInputLength: 0
    });

    // Initialize Select2 for edit modal components
    $('#editDeviceComponents').select2({
        theme: 'bootstrap-5',
        width: '100%',
        ajax: {
            url: '/api/list_component_names',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    search: params.term,
                    page: params.page
                };
            },
            processResults: function (data, params) {
                const term = (params.term || '').toLowerCase();
                const filtered = data.filter(name => 
                    name.toLowerCase().includes(term)
                );
                
                return {
                    results: filtered.map(name => ({
                        id: name,
                        text: name
                    }))
                };
            },
            cache: true
        },
        placeholder: 'Select components',
        allowClear: true,
        tags: true,
        multiple: true,
        minimumInputLength: 0
    });

    // Initialize Select2 for peripherals
    $('#createDevicePeripherals').select2({
        theme: 'bootstrap-5',
        width: '100%',
        ajax: {
            url: '/api/list_peripheral_names',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    search: params.term, // search term
                    page: params.page
                };
            },
            processResults: function (data, params) {
                // Filter results based on search term
                const term = (params.term || '').toLowerCase();
                const filtered = data.filter(name => 
                    name.toLowerCase().includes(term)
                );
                
                return {
                    results: filtered.map(name => ({
                        id: name,
                        text: name
                    }))
                };
            },
            cache: true
        },
        placeholder: 'Select peripherals',
        allowClear: true,
        tags: true,
        multiple: true,
        minimumInputLength: 0
    });

    // Initialize Select2 for edit modal peripherals
    $('#editDevicePeripherals').select2({
        theme: 'bootstrap-5',
        width: '100%',
        ajax: {
            url: '/api/list_peripheral_names',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    search: params.term,
                    page: params.page
                };
            },
            processResults: function (data, params) {
                const term = (params.term || '').toLowerCase();
                const filtered = data.filter(name => 
                    name.toLowerCase().includes(term)
                );
                
                return {
                    results: filtered.map(name => ({
                        id: name,
                        text: name
                    }))
                };
            },
            cache: true
        },
        placeholder: 'Select peripherals',
        allowClear: true,
        tags: true,
        multiple: true,
        minimumInputLength: 0
    });

    // When new device button is clicked
    $('#newDeviceBtn').on('click', function() {
        // Reset form
        $('#createDeviceName').val('');
        $('#createDeviceDescription').val('');
        $('#createDeviceStatus').val('Active');
        $('#createDeviceLocation').val('');
        $('#createDeviceMacAddress').val('');
        $('#createDeviceComponents').val(null).trigger('change');
        $('#createDevicePeripherals').val(null).trigger('change');
        createDeviceModal.show();
    });

    // Function to validate MAC address format
    function isValidMacAddress(mac) {
        if (!mac) return true; // Empty MAC address is allowed
        const macRegex = /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/;
        return macRegex.test(mac);
    }

    // Function to format MAC address (add colons if missing)
    function formatMacAddress(mac) {
        if (!mac) return '';
        // Remove any existing separators
        mac = mac.replace(/[^0-9A-Fa-f]/g, '');
        // Add colons every 2 characters
        return mac.match(/.{1,2}/g).join(':').toUpperCase();
    }

    // When save new device button is clicked
    $('#saveNewDeviceBtn').on('click', function() {
        const macAddress = $('#createDeviceMacAddress').val();
        
        // Validate MAC address if provided
        if (macAddress && !isValidMacAddress(macAddress)) {
            showAlert('Invalid MAC address format. Please use format: XX:XX:XX:XX:XX:XX');
            return;
        }

        const data = {
            name: $('#createDeviceName').val(),
            description: $('#createDeviceDescription').val(),
            status: $('#createDeviceStatus').val(),
            location: $('#createDeviceLocation').val(),
            mac_address: formatMacAddress(macAddress),
            components: $('#createDeviceComponents').val() || [],
            peripherals: $('#createDevicePeripherals').val() || []
        };

        // Validate required fields
        if (!data.name) {
            showAlert('Device name is required.');
            return;
        }

        fetch('/api/device', {
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
            createDeviceModal.hide();
            // Call consolidation endpoints
            Promise.all([
                fetch('/components/consolidate', { method: 'POST' }),
                fetch('/peripherals/consolidate', { method: 'POST' })
            ])
            .then(() => {
                // Reload the page to show the new device
                window.location.reload();
            })
            .catch(error => {
                console.error('Error consolidating inventory:', error);
                // Still reload the page even if consolidation fails
                window.location.reload();
            });
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error creating device. Please try again.');
        });
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

    // Edit device modal handling
    const editModal = new bootstrap.Modal(document.getElementById('editDeviceModal'));

    // When edit button is clicked, populate and show modal
    $('.edit-device-btn').on('click', function() {
        const button = $(this);
        const deviceId = button.data('device-id');
        const deviceName = button.data('device-name');
        const deviceDescription = button.data('device-description');
        const deviceStatus = button.data('device-status');
        const deviceLocation = button.data('device-location');
        const deviceMacAddress = button.data('device-mac-address');
        const deviceComponents = button.data('device-components') ? button.data('device-components').split(',').filter(Boolean) : [];
        const devicePeripherals = button.data('device-peripherals') ? button.data('device-peripherals').split(',').filter(Boolean) : [];

        // Populate modal fields
        $('#editDeviceId').val(deviceId);
        $('#editDeviceName').val(deviceName);
        $('#editDeviceDescription').val(deviceDescription);
        $('#editDeviceStatus').val(deviceStatus);
        $('#editDeviceLocation').val(deviceLocation);
        $('#editDeviceMacAddress').val(deviceMacAddress);
        
        // Destroy existing Select2 instances
        if ($('#editDeviceComponents').data('select2')) {
            $('#editDeviceComponents').select2('destroy');
        }
        if ($('#editDevicePeripherals').data('select2')) {
            $('#editDevicePeripherals').select2('destroy');
        }

        // Pre-populate components
        const componentsData = deviceComponents.map(component => ({
            id: component.trim(),
            text: component.trim()
        }));
        
        // Initialize components Select2
        $('#editDeviceComponents').select2({
            theme: 'bootstrap-5',
            width: '100%',
            data: componentsData,
            ajax: {
                url: '/api/list_component_names',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        search: params.term,
                        page: params.page
                    };
                },
                processResults: function (data, params) {
                    const term = (params.term || '').toLowerCase();
                    const filtered = data.filter(name => 
                        name.toLowerCase().includes(term)
                    );
                    
                    return {
                        results: filtered.map(name => ({
                            id: name,
                            text: name
                        }))
                    };
                },
                cache: true
            },
            placeholder: 'Select components',
            allowClear: true,
            tags: true,
            multiple: true,
            minimumInputLength: 0
        }).val(deviceComponents).trigger('change');

        // Pre-populate peripherals
        const peripheralsData = devicePeripherals.map(peripheral => ({
            id: peripheral.trim(),
            text: peripheral.trim()
        }));
        
        // Initialize peripherals Select2
        $('#editDevicePeripherals').select2({
            theme: 'bootstrap-5',
            width: '100%',
            data: peripheralsData,
            ajax: {
                url: '/api/list_peripheral_names',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        search: params.term,
                        page: params.page
                    };
                },
                processResults: function (data, params) {
                    const term = (params.term || '').toLowerCase();
                    const filtered = data.filter(name => 
                        name.toLowerCase().includes(term)
                    );
                    
                    return {
                        results: filtered.map(name => ({
                            id: name,
                            text: name
                        }))
                    };
                },
                cache: true
            },
            placeholder: 'Select peripherals',
            allowClear: true,
            tags: true,
            multiple: true,
            minimumInputLength: 0
        }).val(devicePeripherals).trigger('change');

        editModal.show();
    });

    // When save button is clicked in edit modal
    $('#saveDeviceBtn').on('click', function() {
        const macAddress = $('#editDeviceMacAddress').val();
        
        // Validate MAC address if provided
        if (macAddress && !isValidMacAddress(macAddress)) {
            showAlert('Invalid MAC address format. Please use format: XX:XX:XX:XX:XX:XX');
            return;
        }

        const deviceId = $('#editDeviceId').val();
        const data = {
            name: $('#editDeviceName').val(),
            description: $('#editDeviceDescription').val(),
            status: $('#editDeviceStatus').val(),
            location: $('#editDeviceLocation').val(),
            mac_address: formatMacAddress(macAddress),
            components: $('#editDeviceComponents').val() || [],
            peripherals: $('#editDevicePeripherals').val() || []
        };

        // Make API call to update device
        fetch(`/api/device/${deviceId}`, {
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
            // Update the table row with new data
            const row = $(`button[data-device-id="${deviceId}"]`).closest('tr');
            row.find('td:eq(0)').text(data.name);
            row.find('td:eq(1) span').text(data.status)
                .removeClass('bg-success bg-warning bg-danger')
                .addClass(getStatusClass(data.status));
            row.find('td:eq(2)').text(data.description || 'N/A');
            row.find('td:eq(3)').text(data.location);

            // Update the edit button's data attributes
            const editBtn = row.find('.edit-device-btn');
            editBtn.data('device-name', data.name);
            editBtn.data('device-description', data.description);
            editBtn.data('device-status', data.status);
            editBtn.data('device-location', data.location);

            // Call consolidation endpoints
            Promise.all([
                fetch('/components/consolidate', { method: 'POST' }),
                fetch('/peripherals/consolidate', { method: 'POST' })
            ])
            .then(() => {
                // Close modal and show success message
                editModal.hide();
                showAlert('Device updated successfully!', 'success');
            })
            .catch(error => {
                console.error('Error consolidating inventory:', error);
                // Still close modal and show success message
                editModal.hide();
                showAlert('Device updated successfully!', 'success');
            });
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error updating device. Please try again.');
        });
    });

    // Create report modal handling
    const createReportModal = new bootstrap.Modal(document.getElementById('createReportModal'));

    $('.create-report-btn').on('click', function() {
        const deviceName = $(this).data('device-name');
        $('#reportDeviceName').val(deviceName);
        $('#reportDeviceNameTitle').text(deviceName);
        $('#reportTitle').val('');
        $('#reportBody').val('');
        createReportModal.show();
    });

    $('#saveReportBtn').on('click', function() {
        const data = {
            title: $('#reportTitle').val(),
            device_name: $('#reportDeviceName').val(),
            status: 'Open',
            body: $('#reportBody').val()
        };

        // Validate required fields
        if (!data.title) {
            showAlert('Report title is required.');
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
            // Optionally redirect to the reports page or refresh the current page
            // window.location.href = '/report';
        })
        .catch(error => {
            // Hide loading overlay
            $('#loadingOverlay').hide();
            console.error('Error:', error);
            showAlert('Error creating report. Please try again.');
        });
    });

    // View device modal handling
    const viewDeviceModal = new bootstrap.Modal(document.getElementById('viewDeviceModal'));

    // When view device button is clicked
    $('.view-device-btn').on('click', function() {
        const deviceId = $(this).data('device-id');
        const deviceName = $(this).data('device-name');

        // Fetch device details
        fetch(`/api/device/${deviceId}`)
            .then(response => response.json())
            .then(device => {
                // Populate device details
                $('#deviceName').text(device.name);
                $('#deviceStatus').html(`<span class="badge ${getStatusClass(device.status)}">${device.status}</span>`);
                $('#deviceLocation').text(device.location || 'N/A');
                $('#deviceMacAddress').text(device.mac_address || 'N/A');
                $('#deviceDescription').text(device.description || 'N/A');

                // Populate components list
                const componentsList = $('#deviceComponents');
                componentsList.empty();
                if (device.components && device.components.length > 0) {
                    device.components.forEach(component => {
                        componentsList.append(`<li>${component}</li>`);
                    });
                } else {
                    componentsList.append('<li>No components listed</li>');
                }

                // Populate peripherals list
                const peripheralsList = $('#devicePeripherals');
                peripheralsList.empty();
                if (device.peripherals && device.peripherals.length > 0) {
                    device.peripherals.forEach(peripheral => {
                        peripheralsList.append(`<li>${peripheral}</li>`);
                    });
                } else {
                    peripheralsList.append('<li>No peripherals listed</li>');
                }

                // Fetch active reports for this device
                fetch(`/api/check_active_reports/${encodeURIComponent(device.name)}`)
                    .then(response => response.json())
                    .then(reports => {
                        const reportsTableBody = $('#activeReportsTableBody');
                        reportsTableBody.empty();

                        if (reports.length > 0) {
                            reports.forEach(report => {
                                const date = new Date(report.created_at).toLocaleString('en-GB', {
                                    day: '2-digit',
                                    month: '2-digit',
                                    year: 'numeric',
                                    hour: '2-digit',
                                    minute: '2-digit'
                                });
                                const description = report.body ? 
                                    (report.body.length > 100 ? report.body.substring(0, 100) + '...' : report.body) 
                                    : 'No description';
                                reportsTableBody.append(`
                                    <tr>
                                        <td class="align-middle">${report.title}</td>
                                        <td class="align-middle">${description}</td>
                                        <td class="align-middle">${date}</td>
                                        <td class="align-middle">${report.author_username}</td>
                                    </tr>
                                `);
                            });
                        } else {
                            reportsTableBody.append('<tr><td colspan="4" class="text-center">No active reports</td></tr>');
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching active reports:', error);
                        $('#activeReportsTableBody').html('<tr><td colspan="4" class="text-center text-danger">Error loading active reports</td></tr>');
                    });
            })
            .catch(error => {
                console.error('Error fetching device details:', error);
                showAlert('Error loading device details. Please try again.');
            });

        viewDeviceModal.show();
    });

    // Helper function to get status badge class
    function getStatusClass(status) {
        switch(status) {
            case 'Active':
                return 'bg-success';
            case 'Maintenance':
                return 'bg-warning';
            default:
                return 'bg-danger';
        }
    }
});
