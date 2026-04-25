$(document).ready(function () {

    // ── Select2 Init ────────────────────────────────────────
    $('select').not('.no-select2').select2({
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