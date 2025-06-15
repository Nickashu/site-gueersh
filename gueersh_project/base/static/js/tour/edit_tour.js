$(function () {
    $("#add-form").on("click", function(){
        let totalForms = $("#id_concerts-TOTAL_FORMS");
        let formCount = parseInt(totalForms.val());
        let newFormHtml = $("#empty-form").html().replace(/__prefix__/g, formCount);
        let $newForm = $("<div class='formset-form mb-3'></div>").append(newFormHtml);

        $("#formset-container").append($("<hr>")).append($newForm);   //Adiciona o novo form ao container
        totalForms.val(formCount + 1);
    });
});
