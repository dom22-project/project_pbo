// Main JavaScript for PBO Web Application

// Document Ready
$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Confirm before form reset
    $('button[type="reset"]').on('click', function(e) {
        if (!confirm('Apakah Anda yakin ingin mereset form? Semua data yang diisi akan hilang.')) {
            e.preventDefault();
        }
    });

    // Format currency inputs on blur
    $('.currency-input').on('blur', function() {
        var value = parseFloat($(this).val()) || 0;
        $(this).val(formatCurrency(value));
    });

    // Remove currency formatting on focus
    $('.currency-input').on('focus', function() {
        var value = $(this).val().replace(/[^0-9]/g, '');
        $(this).val(value);
    });

    // Table row click to view detail
    $('.table-clickable tbody tr').on('click', function() {
        var url = $(this).data('url');
        if (url) {
            window.location.href = url;
        }
    });

    // Smooth scroll to top
    $('#scrollToTop').on('click', function() {
        $('html, body').animate({ scrollTop: 0 }, 'smooth');
    });

    // Show scroll to top button when scrolling
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#scrollToTop').fadeIn();
        } else {
            $('#scrollToTop').fadeOut();
        }
    });

    // Form validation
    $('form').on('submit', function(e) {
        var form = $(this);
        
        // Check required fields
        var isValid = true;
        form.find('[required]').each(function() {
            if (!$(this).val()) {
                isValid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });

        if (!isValid) {
            e.preventDefault();
            showAlert('Mohon lengkapi semua field yang wajib diisi (bertanda *)', 'danger');
            return false;
        }
    });

    // Remove invalid class on input
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid');
    });

    // Number input validation
    $('input[type="number"]').on('input', function() {
        var value = $(this).val();
        if (value < 0) {
            $(this).val(0);
        }
    });

    // Prevent form submission on Enter key (except in textarea)
    $('form input').not('textarea').on('keypress', function(e) {
        if (e.which === 13) {
            e.preventDefault();
            return false;
        }
    });

    // Add loading state to buttons on form submit
    $('form').on('submit', function() {
        $(this).find('button[type="submit"]').prop('disabled', true).html(
            '<span class="spinner-border spinner-border-sm me-2"></span>Menyimpan...'
        );
    });

    // Print functionality
    $('.btn-print').on('click', function(e) {
        e.preventDefault();
        window.print();
    });

    // Confirm delete action
    $('.btn-delete').on('click', function(e) {
        if (!confirm('Apakah Anda yakin ingin menghapus data ini? Data yang dihapus tidak dapat dikembalikan!')) {
            e.preventDefault();
            return false;
        }
    });

    // Search input auto-focus
    if ($('#searchInput').length) {
        $('#searchInput').focus();
    }

    // Table search functionality
    $('#tableSearch').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $('#dataTable tbody tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Export table to CSV
    $('#exportCSV').on('click', function() {
        exportTableToCSV('data_pbo.csv');
    });

    // Add fade-in animation to cards
    $('.card').addClass('fade-in');
});

// Utility Functions

/**
 * Format number as Indonesian Rupiah
 */
function formatCurrency(amount) {
    return 'Rp ' + parseInt(amount).toLocaleString('id-ID');
}

/**
 * Parse currency string to number
 */
function parseCurrency(currencyString) {
    return parseFloat(currencyString.replace(/[^0-9]/g, '')) || 0;
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    var alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('.container').first().prepend(alertHtml);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
}

/**
 * Show loading spinner
 */
function showLoading(element) {
    $(element).addClass('loading');
}

/**
 * Hide loading spinner
 */
function hideLoading(element) {
    $(element).removeClass('loading');
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validate phone number (Indonesian format)
 */
function isValidPhone(phone) {
    var regex = /^(\+62|62|0)[0-9]{9,12}$/;
    return regex.test(phone.replace(/\s/g, ''));
}

/**
 * Format date to Indonesian format
 */
function formatDateIndonesian(dateString) {
    var date = new Date(dateString);
    var months = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ];
    
    return date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear();
}

/**
 * Export table to CSV
 */
function exportTableToCSV(filename) {
    var csv = [];
    var rows = document.querySelectorAll('table tr');
    
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ');
            // Escape double-quote with double-double-quote
            data = data.replace(/"/g, '""');
            // Push escaped string
            row.push('"' + data + '"');
        }
        
        csv.push(row.join(','));
    }
    
    // Download CSV
    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;
    
    // CSV file
    csvFile = new Blob([csv], {type: 'text/csv'});
    
    // Download link
    downloadLink = document.createElement('a');
    
    // File name
    downloadLink.download = filename;
    
    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);
    
    // Hide download link
    downloadLink.style.display = 'none';
    
    // Add the link to DOM
    document.body.appendChild(downloadLink);
    
    // Click download link
    downloadLink.click();
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    var tempInput = document.createElement('input');
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    
    showAlert('Teks berhasil disalin ke clipboard!', 'success');
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    var timeout;
    return function executedFunction(...args) {
        var later = function() {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Check if element is in viewport
 */
function isInViewport(element) {
    var rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Animate number counting
 */
function animateValue(element, start, end, duration) {
    var range = end - start;
    var current = start;
    var increment = end > start ? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var timer = setInterval(function() {
        current += increment;
        element.textContent = current;
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}

/**
 * Get URL parameter
 */
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

/**
 * Scroll to element smoothly
 */
function scrollToElement(element, offset = 0) {
    var elementPosition = $(element).offset().top;
    var offsetPosition = elementPosition - offset;
    
    $('html, body').animate({
        scrollTop: offsetPosition
    }, 500);
}

// Console log for debugging (remove in production)
console.log('PBO Web Application - JavaScript Loaded');
console.log('Version: 1.0.0');
console.log('© 2024 RS Siloam TB Simatupang');
