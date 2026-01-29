/* Adabiyya Smart Connect - Main JavaScript
 * Vanilla JS only - no frameworks
 * Light interactivity for better UX
 */

(function() {
  'use strict';

  // ===== Toast Notifications =====
  function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { autohide: true, delay: 5000 });
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
      toast.remove();
    });
  }

  function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
  }

  // Expose toast function globally
  window.showToast = showToast;

  // ===== Form Validation Enhancement =====
  function enhanceFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
          
          // Show first invalid field error
          const firstInvalid = form.querySelector(':invalid');
          if (firstInvalid) {
            firstInvalid.focus();
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
        
        form.classList.add('was-validated');
      }, false);
    });
  }

  // ===== Auto-dismiss Alerts =====
  function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert[data-auto-dismiss]');
    alerts.forEach(alert => {
      const delay = parseInt(alert.getAttribute('data-auto-dismiss')) || 5000;
      setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }, delay);
    });
  }

  // ===== Table Search =====
  function initTableSearch() {
    const searchInputs = document.querySelectorAll('[data-table-search]');
    
    searchInputs.forEach(input => {
      const tableId = input.getAttribute('data-table-search');
      const table = document.getElementById(tableId);
      
      if (!table) return;
      
      input.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
          const text = row.textContent.toLowerCase();
          row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
      });
    });
  }

  // ===== Confirm Delete Dialogs =====
  function initConfirmDelete() {
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    
    deleteButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        const message = this.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
        if (!confirm(message)) {
          e.preventDefault();
          return false;
        }
      });
    });
  }

  // ===== Loading States for Buttons =====
  function initLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      form.addEventListener('submit', function() {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
          submitButton.disabled = true;
          const originalText = submitButton.innerHTML;
          submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
          
          // Re-enable after 10 seconds as fallback (in case of network issues)
          setTimeout(() => {
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
          }, 10000);
        }
      });
    });
  }

  // ===== Smooth Scroll for Anchor Links =====
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.length > 1) {
          const target = document.querySelector(href);
          if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
      });
    });
  }

  // ===== Initialize on DOM Ready =====
  function init() {
    enhanceFormValidation();
    autoDismissAlerts();
    initTableSearch();
    initConfirmDelete();
    initLoadingStates();
    initSmoothScroll();
    
    // Show toast from Django messages if present
    const messages = document.querySelectorAll('.alert-message');
    messages.forEach(msg => {
      const message = msg.textContent.trim();
      const type = msg.classList.contains('alert-success') ? 'success' :
                   msg.classList.contains('alert-danger') ? 'danger' :
                   msg.classList.contains('alert-warning') ? 'warning' : 'info';
      if (message) {
        showToast(message, type);
      }
    });
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();


