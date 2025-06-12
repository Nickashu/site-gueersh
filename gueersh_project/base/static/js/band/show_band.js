$(function() {
    $('.btn-add, .btn-cancel, .btn-delete').hide();
    $('.btn-edit').show();
    $('.btn-edit').on('click', function() {
        $(this).hide();
        $('.btn-add, .btn-cancel, .btn-delete').show();
    });

    $('.btn-cancel').on('click', function() {
        $(this).hide();
        $('.btn-add, .btn-delete').hide();
        $('.btn-edit').show();
    });
});

function confirmarExclusao() {
    return confirm("Tem certeza que deseja excluir esta banda? Esta ação não pode ser desfeita.");
}