$(document).ready(function () {

    // ── Select2 Init ──────────────────────────────────
    $('.select2-select').select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Select an option',
        allowClear: true,
        closeOnSelect: false
    });

    // Keep search box active after selection
    $('.select2-container').on('select2:select', function (e) {
        const data = e.params.data;
        const $container = $(this);
        setTimeout(function() {
            $container.find('.select2-search__field').focus();
        }, 100);
    });

    // ── Clear Field Buttons ────────────────────────────
    // Add clear button to text inputs
    $('input[type="text"], input[type="email"], input[type="number"], textarea').each(function() {
        const $input = $(this);
        if ($input.closest('.d-flex.gap-2').length > 0) return; // Skip if already in a flex container with buttons
        
        const inputWrapper = $('<div class="position-relative"></div>');
        $input.wrap(inputWrapper);
        
        const $clearBtn = $('<button type="button" class="btn-clear-input" style="position:absolute; right:8px; top:50%; transform:translateY(-50%); background:none; border:none; color:var(--text-3); cursor:pointer; display:none; z-index:10;"><i class="bi bi-x-circle"></i></button>');
        
        $input.after($clearBtn);
        
        // Position adjustment for form-control
        if ($input.hasClass('form-control')) {
            $input.css('padding-right', '30px');
        }
        
        $input.on('input', function() {
            if ($(this).val()) {
                $clearBtn.show();
            } else {
                $clearBtn.hide();
            }
        });
        
        $clearBtn.on('click', function() {
            $input.val('').trigger('change');
            $(this).hide();
        });
        
        // Show clear button if input has value on load
        if ($input.val()) {
            $clearBtn.show();
        }
    });

    // Clear button for Select2 in flex containers (with + button)
    $('.d-flex.gap-2').each(function() {
        const $container = $(this);
        const $select = $container.find('select');
        const $addBtn = $container.find('button[type="button"]');
        
        if ($select.length > 0 && $addBtn.length > 0) {
            const $clearBtn = $('<button type="button" class="btn btn-sm btn-outline-secondary" title="Clear selection"><i class="bi bi-x"></i></button>');
            $addBtn.after($clearBtn);
            
            $clearBtn.on('click', function() {
                $select.val(null).trigger('change');
            });
        }
    });

    // ── Form validation modal ───────────────────────────────
    $(document).on('submit', 'form[novalidate]', function (e) {
        const $form = $(this);
        const missingFields = [];

        $form.find('[required]').each(function () {
            const $field = $(this);
            const value = $field.val();

            if (!value || (Array.isArray(value) && value.length === 0)) {
                const label = $field.closest('.field-group').find('label').text().trim() ||
                              $field.attr('name') || 'This field';
                missingFields.push(label);
                $field.addClass('is-invalid');
            } else {
                $field.removeClass('is-invalid');
            }
        });

        if (missingFields.length > 0) {
            e.preventDefault();
            showValidationModal(missingFields);
            return false;
        }
    });

    $('select').on('change', function () {
        if ($(this).val()) {
            $(this).removeClass('is-invalid');
        }
    });

    // ── Dependent dropdown: Printer → Compatible Supplies ───
    const $printer = $('#id_printer');
    const $supply  = $('#id_supply');

    if ($printer.length && $supply.length) {
        $printer.on('change', function () {
            const id = $(this).val();
            $supply.empty().append('<option value="">-- Select Supply --</option>');
            if (id) {
                $.getJSON(`/api/printer/${id}/compatible-supplies/`, function (data) {
                    data.supplies.forEach(s => {
                        $supply.append(new Option(
                            `${s.name} (${s.sku}) — Stock: ${s.current_stock}`,
                            s.id
                        ));
                    });
                    $supply.trigger('change.select2');
                });
            } else {
                $supply.trigger('change.select2');
            }
        });
    }

    // ── Auto-dismiss alerts ──────────────────────────────────
    setTimeout(() => {
        $('.alert').fadeOut('slow', function () { $(this).remove(); });
    }, 5000);

    // ── Global search ────────────────────────────────────────
    $('#globalSearch').on('keypress', function (e) {
        if (e.which === 13 && $(this).val()) {
            window.location.href = `/supplies/?q=${encodeURIComponent($(this).val())}`;
        }
    });

    // ── Confirm dangerous actions ────────────────────────────
    $(document).on('submit', '.confirm-form', function (e) {
        if (!confirm('Are you sure you want to continue? This action cannot be undone.')) {
            e.preventDefault();
        }
    });
});

// ── Sidebar (mobile) ────────────────────────────────────────
function openSidebar() {
    $('#sidebar').addClass('open');
    $('#sidebarOverlay').addClass('show');
    $('body').css('overflow', 'hidden');
}

function closeSidebar() {
    $('#sidebar').removeClass('open');
    $('#sidebarOverlay').removeClass('show');
    $('body').css('overflow', '');
}

// ── Collapsible Sidebar Sections ───────────────────────
// Restore collapsed state from localStorage
function restoreSidebarState() {
    const savedState = localStorage.getItem('sidebarCollapsed');
    const collapsedSections = savedState ? JSON.parse(savedState) : [];
    
    // First, expand all sections (reset to default)
    document.querySelectorAll('.nav-section').forEach(section => {
        section.classList.remove('collapsed');
        const icon = section.querySelector('.section-title i');
        const items = section.querySelector('.nav-section-items');
        if (icon) {
            icon.classList.remove('bi-chevron-right');
            icon.classList.add('bi-chevron-down');
        }
        if (items) items.style.maxHeight = '500px';
    });
    
    // Then, collapse the ones that were saved
    document.querySelectorAll('.nav-section').forEach(section => {
        const sectionName = section.dataset.section;
        if (collapsedSections.includes(sectionName)) {
            section.classList.add('collapsed');
            const icon = section.querySelector('.section-title i');
            const items = section.querySelector('.nav-section-items');
            if (icon) {
                icon.classList.remove('bi-chevron-down');
                icon.classList.add('bi-chevron-right');
            }
            if (items) items.style.maxHeight = '0';
        }
    });
}

// Save collapsed state to localStorage
function saveSidebarState() {
    const collapsedSections = [];
    document.querySelectorAll('.nav-section.collapsed').forEach(section => {
        const sectionName = section.dataset.section;
        if (sectionName) collapsedSections.push(sectionName);
    });
    localStorage.setItem('sidebarCollapsed', JSON.stringify(collapsedSections));
}

// Restore state on page load
document.addEventListener('DOMContentLoaded', restoreSidebarState);
// Also run after a short delay to ensure it applies
window.addEventListener('load', restoreSidebarState);

function toggleNavSection(el) {
    const section = el.parentElement;
    const items = section.querySelector('.nav-section-items');
    const icon = el.querySelector('.bi-chevron-down') || el.querySelector('.bi-chevron-right');
    
    if (section.classList.contains('collapsed')) {
        section.classList.remove('collapsed');
        icon.classList.remove('bi-chevron-right');
        icon.classList.add('bi-chevron-down');
        items.style.maxHeight = items.scrollHeight + 'px';
    } else {
        section.classList.add('collapsed');
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-right');
        items.style.maxHeight = '0';
    }
    
    // Save state to localStorage
    saveSidebarState();
}

// ── Validation Modal ───────────────────────────────────────
function showValidationModal(fields) {
    const $modal = $('#validationModal');
    const $list = $modal.find('#validationErrorList');
    $list.empty();

    fields.forEach(field => {
        $list.append(`<li style="color:var(--text-2); padding:4px 0;"><i class="bi bi-x-circle-fill me-2" style="color:var(--danger);"></i>${field}</li>`);
    });

    const modal = new bootstrap.Modal($modal[0]);
    modal.show();
}

// Add validation modal to base.html
if (!$('#validationModal').length) {
    $('body').append(`
    <div class="modal fade" id="validationModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content" style="background:var(--surface-2); border:1px solid var(--border-strong);">
                <div class="modal-header" style="border-bottom:1px solid var(--border);">
                    <h5 class="modal-title" style="color:var(--text-1);">
                        <i class="bi bi-exclamation-triangle-fill me-2" style="color:var(--warning);"></i>Required Fields
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p style="color:var(--text-2); margin-bottom:12px;">Please fill in all required fields:</p>
                    <ul id="validationErrorList" style="list-style:none; padding:0; margin:0;"></ul>
                </div>
                <div class="modal-footer" style="border-top:1px solid var(--border);">
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal">OK</button>
                </div>
            </div>
        </div>
    </div>
    `);
}