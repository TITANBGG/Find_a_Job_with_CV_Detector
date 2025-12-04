class CustomNavbar extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        .navbar {
          transition: all 0.3s ease;
        }
        .navbar.scrolled {
          background-color: white;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .nav-link {
          position: relative;
        }
        .nav-link::after {
          content: '';
          position: absolute;
          width: 0;
          height: 2px;
          bottom: -2px;
          left: 0;
          background-color: #6366f1;
          transition: width 0.3s ease;
        }
        .nav-link:hover::after {
          width: 100%;
        }
        .mobile-menu {
          max-height: 0;
          overflow: hidden;
          transition: max-height 0.3s ease-out;
        }
        .mobile-menu.open {
          max-height: 500px;
        }
      </style>
      <nav class="navbar fixed w-full z-10 bg-white md:bg-transparent py-4">
        <div class="container mx-auto px-4">
          <div class="flex justify-between items-center">
            <a href="#" class="text-2xl font-bold text-indigo-600">JD</a>
            
            <!-- Desktop Navigation -->
            <div class="hidden md:flex space-x-8">
              <a href="#about" class="nav-link text-gray-700 hover:text-indigo-600">About</a>
              <a href="#experience" class="nav-link text-gray-700 hover:text-indigo-600">Experience</a>
              <a href="#projects" class="nav-link text-gray-700 hover:text-indigo-600">Projects</a>
              <a href="#contact" class="nav-link text-gray-700 hover:text-indigo-600">Contact</a>
            </div>
            
            <!-- Mobile menu button -->
            <button class="md:hidden focus:outline-none" id="mobile-menu-button">
              <i data-feather="menu"></i>
            </button>
          </div>
          
          <!-- Mobile Navigation -->
          <div class="mobile-menu md:hidden" id="mobile-menu">
            <div class="flex flex-col space-y-4 mt-4">
              <a href="#about" class="nav-link text-gray-700 hover:text-indigo-600">About</a>
              <a href="#experience" class="nav-link text-gray-700 hover:text-indigo-600">Experience</a>
              <a href="#projects" class="nav-link text-gray-700 hover:text-indigo-600">Projects</a>
              <a href="#contact" class="nav-link text-gray-700 hover:text-indigo-600">Contact</a>
            </div>
          </div>
        </div>
      </nav>
    `;

    // Add scroll effect
    const navbar = this.shadowRoot.querySelector('.navbar');
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });

    // Mobile menu toggle
    const mobileMenuButton = this.shadowRoot.getElementById('mobile-menu-button');
    const mobileMenu = this.shadowRoot.getElementById('mobile-menu');
    
    mobileMenuButton.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      feather.replace();
    });

    // Close mobile menu when clicking a link
    const mobileLinks = this.shadowRoot.querySelectorAll('#mobile-menu a');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
      });
    });
  }
}

customElements.define('custom-navbar', CustomNavbar);