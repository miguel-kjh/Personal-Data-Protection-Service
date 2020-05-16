$(document).ready(function () {
    const server = "http://127.0.0.1:5000"
    setInterval(setTime, 5);
    function setTime() {
        switch ($("#sel").val()) {
            case "1":
                $('#formId').attr('action', server+'/search/file/extract-data/json-file'); 
                break;
            case "2":
                $('#formId').attr('action', server+'/search/file/encode');
                break;
            case "3":
                $('#formId').attr('action', server+'/search/file/extract-data/zip');       
                break;
            default:
                $('#formId').attr('action', server+'/search/file/tagger-html');    
        }
    }

    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });

    $("#form_web").attr('action', server+'/search/file/operation-web');
});