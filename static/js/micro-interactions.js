/**
 * Premium Micro-Interactions & Loading States
 * Makes the app feel human-designed and polished
 */

(function() {
    'use strict';

    // ============================================
    // BUTTON LOADING STATES
    // ============================================
    function initButtonLoadingStates() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn && !submitBtn.disabled) {
                    // Add loading state
                    submitBtn.classList.add('btn-loading');
                    submitBtn.disabled = true;
                    
                    // Create spinner
                    const spinner = document.createElement('span');
                    spinner.className = 'btn-spinner';
                    spinner.innerHTML = '<i class="bi bi-arrow-repeat"></i>';
                    
                    // Store original content
                    const originalHTML = submitBtn.innerHTML;
                    submitBtn.dataset.originalHtml = originalHTML;
                    
                    // Add spinner
                    submitBtn.innerHTML = spinner.outerHTML + ' Processing...';
                }
            });
        });
    }

    // ============================================
    // RIPPLE EFFECT ON BUTTONS
    // ============================================
    function initRippleEffect() {
        const buttons = document.querySelectorAll('.btn, .card, .stat-card');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                // Don't add ripple to disabled buttons
                if (this.disabled || this.classList.contains('btn-loading')) return;
                
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    // ============================================
    // SMOOTH SCROLL
    // ============================================
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href !== '#' && document.querySelector(href)) {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ============================================
    // FORM FIELD FOCUS ANIMATIONS
    // ============================================
    function initFormFieldAnimations() {
        const inputs = document.querySelectorAll('.form-control, .form-select');
        
        inputs.forEach(input => {
            // Add floating label effect
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement.classList.remove('focused');
                }
            });
            
            // Check if has value on load
            if (input.value) {
                input.parentElement.classList.add('focused');
            }
        });
    }

    // ============================================
    // CARD HOVER ENHANCEMENTS
    // ============================================
    function initCardInteractions() {
        const cards = document.querySelectorAll('.card, .stat-card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }

    // ============================================
    // TOAST NOTIFICATIONS
    // ============================================
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);
        
        // Remove after delay
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // ============================================
    // SKELETON LOADERS
    // ============================================
    function createSkeletonLoader(count = 3) {
        const skeleton = document.createElement('div');
        skeleton.className = 'skeleton-loader';
        skeleton.innerHTML = Array(count).fill(0).map(() => `
            <div class="skeleton-item">
                <div class="skeleton-line skeleton-title"></div>
                <div class="skeleton-line skeleton-text"></div>
                <div class="skeleton-line skeleton-text short"></div>
            </div>
        `).join('');
        return skeleton;
    }

    // ============================================
    // SUCCESS CHECKMARK ANIMATION
    // ============================================
    function showSuccessCheckmark(element) {
        const checkmark = document.createElement('div');
        checkmark.className = 'success-checkmark';
        checkmark.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
        element.appendChild(checkmark);
        
        setTimeout(() => {
            checkmark.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            checkmark.classList.remove('show');
            setTimeout(() => checkmark.remove(), 300);
        }, 2000);
    }

    // ============================================
    // PAGE TRANSITION EFFECTS
    // ============================================
    function initPageTransitions() {
        // Add fade-in animation to main content
        const mainContent = document.querySelector('.container');
        if (mainContent) {
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                mainContent.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';
            }, 50);
        }
    }

    // ============================================
    // PROGRESS BAR ANIMATION
    // ============================================
    function animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const width = bar.style.width || bar.getAttribute('aria-valuenow') + '%';
                    bar.style.width = '0%';
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 100);
                    observer.unobserve(bar);
                }
            });
        }, { threshold: 0.1 });
        
        progressBars.forEach(bar => observer.observe(bar));
    }

    // ============================================
    // TABLE ROW ANIMATIONS
    // ============================================
    function initTableRowAnimations() {
        const tableRows = document.querySelectorAll('tbody tr');
        
        tableRows.forEach((row, index) => {
            row.style.opacity = '0';
            row.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                row.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                row.style.opacity = '1';
                row.style.transform = 'translateX(0)';
            }, index * 50);
        });
    }

    // ============================================
    // STAT CARD COUNTER ANIMATION
    // ============================================
    function animateStatValues() {
        const statValues = document.querySelectorAll('.stat-value');
        
        statValues.forEach(stat => {
            const text = stat.textContent.trim();
            const number = parseFloat(text.replace(/[^\d.]/g, ''));
            
            if (!isNaN(number)) {
                const duration = 1500;
                const steps = 60;
                const increment = number / steps;
                let current = 0;
                
                const observer = new IntersectionObserver((entries) => {
                    if (entries[0].isIntersecting) {
                        const timer = setInterval(() => {
                            current += increment;
                            if (current >= number) {
                                stat.textContent = text; // Restore original with formatting
                                clearInterval(timer);
                            } else {
                                const suffix = text.replace(/[\d.]/g, '');
                                stat.textContent = Math.floor(current) + suffix;
                            }
                        }, duration / steps);
                        observer.unobserve(stat);
                    }
                }, { threshold: 0.5 });
                
                observer.observe(stat);
            }
        });
    }

    // ============================================
    // DELETE CONFIRMATION WITH ANIMATION
    // ============================================
    function initDeleteAnimations() {
        const deleteButtons = document.querySelectorAll('button[type="submit"][onclick*="confirm"]');
        
        deleteButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this?')) {
                    e.preventDefault();
                    return false;
                }
                
                // Add deleting animation
                this.classList.add('deleting');
                this.innerHTML = '<i class="bi bi-hourglass-split"></i> Deleting...';
            });
        });
    }

    // ============================================
    // INPUT VALIDATION FEEDBACK
    // ============================================
    function initInputValidation() {
        const inputs = document.querySelectorAll('.form-control, .form-select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                } else if (this.value) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    }

    // ============================================
    // LAZY LOAD IMAGES (if any)
    // ============================================
    function initLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('fade-in');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }

    // ============================================
    // INITIALIZE ALL FEATURES
    // ============================================
    document.addEventListener('DOMContentLoaded', function() {
        initButtonLoadingStates();
        initRippleEffect();
        initSmoothScroll();
        initFormFieldAnimations();
        initCardInteractions();
        initPageTransitions();
        animateProgressBars();
        initTableRowAnimations();
        animateStatValues();
        initDeleteAnimations();
        initInputValidation();
        initLazyLoading();
        
        // Show success toast for successful form submissions
        const successMessages = document.querySelectorAll('.alert-success');
        successMessages.forEach(alert => {
            setTimeout(() => {
                alert.style.transform = 'translateX(0)';
                alert.style.opacity = '1';
            }, 100);
        });
    });

    // Export functions for use in templates
    window.CalorieTracker = {
        showToast: showToast,
        showSuccessCheckmark: showSuccessCheckmark,
        createSkeletonLoader: createSkeletonLoader
    };

})();
