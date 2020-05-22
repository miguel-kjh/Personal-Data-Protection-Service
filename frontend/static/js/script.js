const server     = "http://127.0.0.1:5000";
const fileFormat = /^(txt|pdf|xls|docx|xlsx|xlsm|html|csv)$/;
const urlRegex   = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/;


$(document).ready(function () {
    setInterval(setTime, 500);
    setInterval(CheckFileExtension, 10);
    function setTime() {
        switch ($("#sel").val()) {
            case "1":
                $('#formId').attr('action', server+'/search/file/extract-data/json-file'); 
                break;
            case "2":
                $('#formId').attr('action', server+'/search/file/encode');
                break;
            case "3":
                $('#formId').attr('action', server+'/search/file/extract-data/csv');       
                break;
            default:
                $('#formId').attr('action', server+'/search/file/tagger-html');    
        }
    }

    function CheckFileExtension() {
        let ext = $("#customFile").val().split('.').pop();
        if (ext.match(fileFormat)) {
            $('.file_upload').prop('disabled', false);
            $('#alert').text("");
        } else {
            $('.file_upload').prop('disabled', true);
            $('#alert').text("* Solo estan permitidos los siguientes formatos: txt, pdf, xls, docx, xlsx, xlsm, html y csv");
        }
    }

    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });

    $("#form_web").attr('action', server+'/search/file/operation-web');
});

function validateForm() {
    let web = $("#url_web").val();
    if (web.match(urlRegex)) {
        $('#url_web').removeClass('error');
        return true;
    } else {
        $('#url_web').addClass('error');
        return false;   
    }
}

