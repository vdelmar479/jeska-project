document.addEventListener('DOMContentLoaded', function() {
    // Get the current URL path
    const currentPath = window.location.pathname;
    
    // Get all sidebar navigation links (both main nav and submenu)
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    const submenuLinks = document.querySelectorAll('.submenu a');
    
    // Function to handle active state
    const setActiveState = (link) => {
        const href = link.getAttribute('href');
        if (currentPath === href) {
            link.classList.add('active');
            link.style.color = '#000';
            
            // If this is a submenu item, also style the parent dropdown
            if (link.closest('.submenu')) {
                const dropdownToggle = link.closest('.collapse').previousElementSibling;
                if (dropdownToggle) {
                    dropdownToggle.style.color = '#000';
                    dropdownToggle.classList.add('active');
                }
            }
        }
    };
    
    // Check regular navigation links
    sidebarLinks.forEach(setActiveState);
    
    // Check submenu links
    submenuLinks.forEach(setActiveState);
});
