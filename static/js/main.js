// Main JavaScript for SecureVault

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach((msg, index) => {
        setTimeout(() => {
            msg.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => {
                if (msg.parentNode) {
                    msg.remove();
                }
            }, 300);
        }, 5000 + (index * 200));
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation enhancement - removed duplicate, see below

// File input preview
document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            const file = this.files[0];
            const fileSize = file.size;
            const maxSize = 100 * 1024 * 1024; // 100MB
            
            if (fileSize > maxSize) {
                alert('File size exceeds 100MB limit. Please choose a smaller file.');
                this.value = '';
                return;
            }
        }
    });
});

// Modal functionality
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal on overlay click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', function(e) {
        if (e.target === this) {
            this.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});

// Close modal on ESC key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(modal => {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
});

// Search functionality (if search input exists)
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        const items = document.querySelectorAll('[data-filename], [data-search]');
        
        items.forEach(item => {
            const searchableText = item.getAttribute('data-filename') || 
                                  item.getAttribute('data-search') || 
                                  item.textContent.toLowerCase();
            
            if (searchableText.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Confirm delete actions
document.querySelectorAll('form[action*="delete"]').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!confirm('Are you sure you want to delete this? This action cannot be undone.')) {
            e.preventDefault();
        }
    });
});

// Add loading states to buttons (only after form starts submitting)
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
            // Don't prevent form submission, just add visual feedback
            submitBtn.disabled = true;
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span>⏳ Processing...</span>';
            
            // Re-enable after 10 seconds (fallback in case form doesn't submit)
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 10000);
        }
    });
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and file items
document.querySelectorAll('.file-card, .stat-card, .card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(el);
});

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success feedback
        const toast = document.createElement('div');
        toast.className = 'flash-message success';
        toast.textContent = 'Copied to clipboard!';
        toast.style.position = 'fixed';
        toast.style.top = '20px';
        toast.style.right = '20px';
        toast.style.zIndex = '9999';
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Export functions for use in templates
window.SecureVault = {
    openModal,
    closeModal,
    copyToClipboard
};

