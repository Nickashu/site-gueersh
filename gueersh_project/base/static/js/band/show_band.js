$(function() {
    $('.btn-add, .btn-cancel, .btn-delete').hide();
    $('.btn-edit').show();
    $('.btn-edit-social').on('click', function() {
        $(this).hide();
        $('.btn-add-social, .btn-cancel-social, .btn-delete-social').show();
    });

    $('.btn-cancel-social').on('click', function() {
        $(this).hide();
        $('.btn-add-social, .btn-delete-social').hide();
        $('.btn-edit-social').show();
    });

    $('.btn-edit-contact').on('click', function() {
        $(this).hide();
        $('.btn-add-contact, .btn-cancel-contact, .btn-delete-contact').show();
    });

    $('.btn-cancel-contact').on('click', function() {
        $(this).hide();
        $('.btn-add-contact, .btn-delete-contact').hide();
        $('.btn-edit-contact').show();
    });
});

function confirmarExclusaoBanda() {
    return confirm("Tem certeza que deseja excluir esta banda? Esta ação não pode ser desfeita.");
}
function confirmarExclusaoTurne() {
    return confirm("Tem certeza que deseja excluir esta turnê? Esta ação não pode ser desfeita.");
}