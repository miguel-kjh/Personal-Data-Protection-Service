const server     = "http://127.0.0.1:5000";
const fileFormat = /^(txt|pdf|xls|docx|xlsx|xlsm|csv)$/;
const urlRegex   = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/;
let id = ""
let idUrl = ""
let fileType = ""
let fileTypeUrl = ""


$(document).ready(function () {

    $("#spinner").hide();
    $("#spinner_web").hide();
    $("#getDocumentButton").hide();
    $("#getUrlButton").hide();


    function getUrlServer() {
        let url = "";
        switch ($("#sel").val()) {
            case "1":
                url = server+'/search/file/extract-data/json-file';
                break;
            case "2":
                url = server+'/search/file/encode';
                break;
            case "3":
                url = server+'/search/file/extract-data/csv';
                break;
            case "4":
                url =  server+'/search/file/disintegration';
                break;
            case "5":
                url =  server+'/search/file/obfuscation';
                break;
        }
        return url;
    }

    $(".custom-file-input").on("change", function() {
        let fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });


    $("#getDocumentButton").on('click', function () {
        
        if (fileType == "json") {
            $.ajax({
                url: server+'/search/file/download?id='+id,
                type: 'GET',
                success: function(data){ 
                    let a = document.createElement('a');
                    let url = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
                    a.href = url;
                    a.download = 'doc.json';
                    document.body.append(a);
                    a.click();
                    a.remove();
                    $('.file_upload').prop('disabled', false);
                    $("#getDocumentButton").hide();
                },
                error: function(jqXHR,exception) {
                    alert(getError(jqXHR,exception))
                    $('.file_upload').prop('disabled', false);
                    $("#getDocumentButton").hide();
                }
            });
        } else {
            $.ajax({
                url: server+'/search/file/download?id='+id,
                type: 'GET',
                xhrFields: {
                    responseType: 'blob'
                },
                success: function(data){ 
                    let a = document.createElement('a');
                    let url = window.URL.createObjectURL(data);
                    a.href = url;
                    a.download = 'doc.' + fileType;
                    document.body.append(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    $('.file_upload').prop('disabled', false);
                    $("#getDocumentButton").hide();
                },
                error: function(jqXHR,exception) {
                    alert(getError(jqXHR,exception))
                    $('.file_upload').prop('disabled', false);
                    $("#getDocumentButton").hide();
                }
            });
    
        }
    });


    $("#getUrlButton").on('click', function () {
        if (fileTypeUrl == "json") {
            $.ajax({
                url: server+'/search/file/download?id='+idUrl,
                type: 'GET',
                success: function(data){ 
                    let a = document.createElement('a');
                    let url = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
                    a.href = url;
                    a.download = 'doc.json';
                    document.body.append(a);
                    a.click();
                    a.remove();
                    $('#html_upload').prop('disabled', false);
                    $("#getUrlButton").hide();
                },
                error: function(jqXHR,exception) {
                    alert(getError(jqXHR,exception))
                    $('#html_upload').prop('disabled', false);
                    $("#getUrlButton").hide();
                }
            });
        } else if(fileTypeUrl == "csv"){
            $.ajax({
                url: server+'/search/file/download?id='+idUrl,
                type: 'GET',
                xhrFields: {
                    responseType: 'blob'
                },
                success: function(data){ 
                    let a = document.createElement('a');
                    let url = window.URL.createObjectURL(data);
                    a.href = url;
                    a.download = 'doc.' + fileTypeUrl;
                    document.body.append(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    $('#html_upload').prop('disabled', false);
                    $("#getUrlButton").hide();
                },
                error: function(jqXHR,exception) {
                    alert(getError(jqXHR,exception));
                    $('#html_upload').prop('disabled', false);
                    $("#getUrlButton").hide();
                }
            });
    
        } else {
            $.ajax({
                url: server+'/search/file/download?id='+idUrl,
                type: 'GET',
                success: function(data){ 
                    let a = document.createElement('a');
                    let url = "data:text/html;charset=utf-8," + encodeURIComponent(data);
                    a.href = url;
                    a.download = 'doc.html';
                    document.body.append(a);
                    a.click();
                    a.remove();
                    $('#html_upload').prop('disabled', false);
                    $("#getUrlButton").hide();
                },
                error: function(jqXHR,exception) {
                    alert(getError(jqXHR,exception));
                    $('#html_upload').prop('disabled', false);
                    $("#getUrlButton").hide();
                }
            });
        }
    });


    $("#formId").submit(function(e) {

        e.preventDefault(); 
    
        if (!checkFileExtension()) {
            return;
        }

        $("#spinner").show();
        $('.file_upload').prop('disabled', true);

        let url  = getUrlServer();
        let formData = new FormData(this);
    
        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            success: function(data)
            {
                id = data.id;
                fileType = data.fileType;
                console.log("Documento con exito!!!")
                console.log(id)
                console.log(fileType)
                $("#getDocumentButton").show();
                $("#spinner").hide();
            },
            error: function(jqXHR,exception){
                alert(getError(jqXHR,exception))
                $("#spinner").hide();
                $('.file_upload').prop('disabled', false);
            },
            cache: false,
            contentType: false,
            processData: false
        });

    });


    $("#form_web").submit(function(e) {

        e.preventDefault(); 
        if (!validateForm()) {
            return;
        }

        $("#spinner_web").show();
        $('#html_upload').prop('disabled', true);

        let url  = server+'/search/file/operation-web?url='+$("#url_web").val()+"&op="+$("#op").val();
        console.log(url);
        $.ajax({
            type: "GET",
            url: url,
            success: function(data)
            {
                idUrl = data.id;
                fileTypeUrl = data.fileType;
                console.log("URL con exito!!!")
                console.log(idUrl)
                console.log(fileTypeUrl)
                $("#getUrlButton").show();
                $("#spinner_web").hide();
            },
            error: function(jqXHR,exception){
                alert(getError(jqXHR,exception))
                $("#spinner_web").hide();
            }
        });
    });


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

function checkFileExtension() {
    let ext = $("#customFile").val().split('.').pop();
    if (ext.match(fileFormat)) {
        $('#alert').text("");
        return true;   
    } else {
        $('#alert').text("* Solo estan permitidos los siguientes formatos: txt, pdf, xls, docx, xlsx, xlsm y csv");
        return false;   
    }
}

function getError(jqXHR,exception){
    let msg = '';
    if (jqXHR.status === 0) {
        msg = 'Not connect.\nVerify Network.';
    } else if (jqXHR.status == 404) {
        msg = 'Requested page not found. [404]';
    } else if (jqXHR.status == 500) {
        msg = 'Internal Server Error [500].';
    } else if (exception === 'parsererror') {
        msg = 'Requested JSON parse failed.';
    } else if (exception === 'timeout') {
        msg = 'Time out error.';
    } else if (exception === 'abort') {
        msg = 'Ajax request aborted.';
    } else {
        msg = 'Uncaught Error.\n' + jqXHR.responseText;
    }
    return msg;
}

