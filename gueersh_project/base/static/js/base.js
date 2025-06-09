$(function () {
    if ($('.main-page').length > 0) {
        logo = $(".logo-header");
        $(logo).addClass('logo-header-anim');
    }

    $(document).on("submit", "#newsletter-form", function (e) {
        e.preventDefault();

        var form = $(this);
        var url = form.data("url");
        console.log("Enviando formulário para: " + url);
        var formData = form.serialize();

        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"  //Para o Django saber que é AJAX
            },
            success: function (response) {
                $("#newsletter-feedback").removeClass().addClass("alert alert-" + response.status).text(response.message).hide().fadeIn();
                
                if (response.status === "success")
                    form.trigger("reset");
            },
            error: function () {
                $("#newsletter-feedback").removeClass().addClass("alert alert-danger").text("Erro ao enviar. Tente novamente.").hide().fadeIn();
            }
        });
    });

    checkForMessages();
});

function checkForMessages() {
    var $container = $("#toast-container");
    if (!$container.length) return;

    var messages = $container.data("messages");
    if (!Array.isArray(messages)) return;

    messages.forEach(function (msg) {
        var toast = `
        <div class="toast align-items-center text-white bg-${msg.tags} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="3000">
            <div class="d-flex">
            <div class="toast-body">
                ${msg.text}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Fechar"></button>
            </div>
        </div>
        `;
        $container.append(toast);
    });

    $('.toast').each(function () {
        var toast = new bootstrap.Toast(this);
        toast.show();
    });
}
