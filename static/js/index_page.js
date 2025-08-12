




// Event listener for the Text Input card
document.querySelector('.card[data-id="1"]').addEventListener('click', () => {
    window.location.assign("/text-to-video");
});
// Event listener for the Custom Input card
document.querySelector('.card[data-id="2"]').addEventListener('click', () => {
    window.location.assign("/multi-model-template");
});

// Event listener for the CSV Input card
document.addEventListener('DOMContentLoaded', () => {
    const card = document.querySelector('.card[data-id="3"]');
    console.log("Card element:", card); // Check if the card is selected
    if (card) {
        card.addEventListener('click', () => {
            console.log("CSV Input card clicked!"); // Confirm click event
            try {
                window.location.assign("/csv-to-video");
                console.log("Navigating to /csv-to-video...");
            } catch (error) {
                console.error("Navigation error:", error);
            }
        });
    } else {
        console.error("Card element not found!");
    }
});

    // Navbar mobile menu toggle
    document.addEventListener('DOMContentLoaded', function () {
        const toggleBtn = document.getElementById('navbar-toggle');
        const mobileMenu = document.getElementById('navbar-mobile-menu');
        if (toggleBtn && mobileMenu) {
            let menuOpen = false;
            toggleBtn.addEventListener('click', function () {
                menuOpen = !menuOpen;
                if (menuOpen) {
                    mobileMenu.style.maxHeight = '400px';
                    const svg = toggleBtn.querySelector('svg');
                    if (svg) svg.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>';
                } else {
                    mobileMenu.style.maxHeight = '0';
                    const svg = toggleBtn.querySelector('svg');
                    if (svg) svg.innerHTML = '<path id="navbar-toggle-icon" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>';
                }
            });
            // Close menu on link click (mobile)
            Array.from(mobileMenu.querySelectorAll('a')).forEach(link => {
                link.addEventListener('click', () => {
                    menuOpen = false;
                    mobileMenu.style.maxHeight = '0';
                    const svg = toggleBtn.querySelector('svg');
                    if (svg) svg.innerHTML = '<path id="navbar-toggle-icon" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>';
                });
            });
        }
    });

// Enhance navbar interactions without changing existing behavior
document.addEventListener('DOMContentLoaded', () => {
        const navbar = document.getElementById('tm-nav') || document.querySelector('.ai-navbar');
        const mobileMenu = document.getElementById('navbar-mobile-menu');
        const toggleBtn = document.getElementById('navbar-toggle');
        const bsToggleBtn = document.querySelector('#tm-nav .navbar-toggler');
        const bsCollapse = document.getElementById('navbarNav');
    const setScrolledState = () => {
        if (!navbar) return;
        if (window.scrollY > 8) {
                navbar.classList.add('scrolled', 'navbar-blur', 'navbar-shadow');
        } else {
                navbar.classList.remove('scrolled', 'navbar-blur', 'navbar-shadow');
        }
    };
    setScrolledState();
    window.addEventListener('scroll', setScrolledState, { passive: true });

    // Sync active state with current path for robustness
    const currentPath = window.location.pathname;
    const maybeMarkActive = (anchor) => {
        const href = anchor.getAttribute('href');
        if (!href) return;
        // Exact match for root, prefix match for subpaths
        const isActive = (href === '/' && currentPath === '/') ||
                         (href !== '/' && currentPath.startsWith(href));
            if (isActive) {
                anchor.classList.add('active');
                const li = anchor.closest('li');
                if (li) li.classList.add('active');
            } else {
                anchor.classList.remove('active');
                const li = anchor.closest('li');
                if (li) li.classList.remove('active');
            }
    };
        const navScope = navbar || document;
        navScope.querySelectorAll('a.navbar-link, .ai-navbar a, .nav-link').forEach(maybeMarkActive);

    // Make mobile menu responsive if Tailwind utility isn't present
        if (toggleBtn && mobileMenu) {
        toggleBtn.addEventListener('click', () => {
            const isOpen = mobileMenu.style.maxHeight && mobileMenu.style.maxHeight !== '0px';
            // Expand to viewport height minus navbar for a drawer-like panel
            const nav = document.querySelector('.ai-navbar');
            const navH = nav ? nav.getBoundingClientRect().height : 56;
            const viewportH = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
            const target = Math.max(280, viewportH - navH - 8);
            mobileMenu.style.maxHeight = isOpen ? '0px' : `${target}px`;
        });
        // Close on route click
        Array.from(mobileMenu.querySelectorAll('a')).forEach(a => a.addEventListener('click', () => {
            mobileMenu.style.maxHeight = '0px';
        }));
    }

        // Bootstrap navbar support: collapse on link click (if using #navbarNav)
        const bsNav = document.getElementById('navbarNav');
        if (bsNav) {
            bsNav.querySelectorAll('a').forEach(a => {
                a.addEventListener('click', () => {
                    // If Bootstrap collapse is open, let it close via data attributes; no manual JS required.
                    // We still update active states proactively.
                    navScope.querySelectorAll('a.navbar-link, .nav-link').forEach(el => el.classList.remove('active'));
                    a.classList.add('active');
                    // Manually close if Bootstrap JS is not present
                    if (bsCollapse && bsCollapse.classList.contains('show')) {
                        bsCollapse.classList.remove('show');
                    }
                });
            });
        }

        // Fallback toggle for Bootstrap collapse if Bootstrap JS/Popper are unavailable
        if (bsToggleBtn && bsCollapse) {
            bsToggleBtn.addEventListener('click', (e) => {
                // If Bootstrap has handled it, this will be redundant but harmless
                bsCollapse.classList.toggle('show');
            });
        }
});