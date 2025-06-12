document.addEventListener('DOMContentLoaded', function() {
    // Function to create a new input group
    function createInputGroup(name) {
        const div = document.createElement('div');
        div.className = 'input-group mb-2';
        div.innerHTML = `
            <input type="text" class="form-control" name="${name}[]">
            <button type="button" class="btn btn-danger remove-item">Remove</button>
        `;
        return div;
    }

    // Add event listeners for "Add" buttons
    document.getElementById('addLocation').addEventListener('click', () => {
        document.getElementById('locationsList').appendChild(createInputGroup('locations'));
    });

    document.getElementById('addDeviceStatus').addEventListener('click', () => {
        document.getElementById('deviceStatusesList').appendChild(createInputGroup('deviceStatuses'));
    });

    document.getElementById('addReportStatus').addEventListener('click', () => {
        document.getElementById('reportStatusesList').appendChild(createInputGroup('reportStatuses'));
    });

    document.getElementById('addComponentType').addEventListener('click', () => {
        document.getElementById('componentTypesList').appendChild(createInputGroup('componentTypes'));
    });

    document.getElementById('addPeripheralType').addEventListener('click', () => {
        document.getElementById('peripheralTypesList').appendChild(createInputGroup('peripheralTypes'));
    });

    // Add event listeners for remove buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-item')) {
            e.target.parentElement.remove();
        }
    });

    // Function to handle form submissions
    async function handleFormSubmit(formId, endpoint) {
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        const values = Array.from(formData.getAll(formData.keys().next().value));

        try {
            const response = await fetch(`/configuration/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ values }),
            });

            if (response.ok) {
                alert('Configuration updated successfully!');
            } else {
                throw new Error('Failed to update configuration');
            }
        } catch (error) {
            alert('Error updating configuration: ' + error.message);
        }
    }

    // Add form submit handlers
    document.getElementById('locationsForm').addEventListener('submit', (e) => {
        e.preventDefault();
        handleFormSubmit('locationsForm', 'update-locations');
    });

    document.getElementById('deviceStatusesForm').addEventListener('submit', (e) => {
        e.preventDefault();
        handleFormSubmit('deviceStatusesForm', 'update-device-statuses');
    });

    document.getElementById('reportStatusesForm').addEventListener('submit', (e) => {
        e.preventDefault();
        handleFormSubmit('reportStatusesForm', 'update-report-statuses');
    });

    document.getElementById('componentTypesForm').addEventListener('submit', (e) => {
        e.preventDefault();
        handleFormSubmit('componentTypesForm', 'update-component-types');
    });

    document.getElementById('peripheralTypesForm').addEventListener('submit', (e) => {
        e.preventDefault();
        handleFormSubmit('peripheralTypesForm', 'update-peripheral-types');
    });
});
