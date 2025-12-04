class CustomFooter extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        .footer-link:hover {
          color: #6366f1;
          transform: translateY(-2px);
        }
        .footer-link {
          transition: all 0.3s ease;
        }
      </style>
      <footer class="bg-gray-800 text-white py-12">
        <div class="container mx-auto px-4">
          <div class="flex flex-col md:flex-row justify-between items-center">
            <div class="mb-8 md:mb-0">
              <h2 class="text-2xl font-bold mb-4">John Doe</h2>
              <p class="text-gray-400 max-w-md">Creating beautiful, functional websites that help businesses grow and succeed in the digital world.</p>
            </div>
            
            <div class="grid grid-cols-2 gap-8">
              <div>
                <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
                <ul class="space-y-2">
                  <li><a href="#about" class="footer-link text-gray-400">About</a></li>
                  <li><a href="#experience" class="footer-link text-gray-400">Experience</a></li>
                  <li><a href="#projects" class="footer-link text-gray-400">Projects</a></li>
                  <li><a href="#contact" class="footer-link text-gray-400">Contact</a></li>
                </ul>
              </div>
              
              <div>
                <h3 class="text-lg font-semibold mb-4">Connect</h3>
                <ul class="space-y-2">
                  <li><a href="#" class="footer-link text-gray-400 flex items-center gap-2"><i data-feather="github"></i> GitHub</a></li>
                  <li><a href="#" class="footer-link text-gray-400 flex items-center gap-2"><i data-feather="linkedin"></i> LinkedIn</a></li>
                  <li><a href="#" class="footer-link text-gray-400 flex items-center gap-2"><i data-feather="twitter"></i> Twitter</a></li>
                  <li><a href="#" class="footer-link text-gray-400 flex items-center gap-2"><i data-feather="mail"></i> Email</a></li>
                </ul>
              </div>
            </div>
          </div>
          
          <div class="border-t border-gray-700 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; ${new Date().getFullYear()} John Doe. All rights reserved.</p>
          </div>
        </div>
      </footer>
    `;
  }
}

customElements.define('custom-footer', CustomFooter);