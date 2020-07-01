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

    function getTypeOfPersonalData() {
        /**
         * Gets the data type from the checkbox 
         * returns String
         */

        if ($('#names').is(":checked") && $('#idCards').is(":checked")) {
            return "all";
        }
        if($('#names').is(":checked")) return "names";
        if($('#idCards').is(":checked")) return "idCards";
        return null;
    }

    function getUrlServer(personalData) {
        /**
         * Obtains the type of operation to be carried out 
         * return String
         */

        let url = "";
        switch ($("#sel").val()) {
            case "1":
                url = server+'/search/file/extract-data/json-file?personalData='+personalData;
                break;
            case "2":
                url = server+'/search/file/encode?personalData='+personalData;
                break;
            case "3":
                url = server+'/search/file/extract-data/csv?personalData='+personalData;
                break;
            case "4":
                url = server+'/search/file/disintegration?personalData='+personalData;
                break;
            case "5":
                url = server+'/search/file/obfuscation?personalData='+personalData;
                break;
        }
        return url;
    }

    $(".custom-file-input").on("change", function() {
        // Analyzes the file path and displays only its name in the form

        let fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });

    function createModalError(jqXHR,exception) {
        /**
         * Creates a window to display the error
         */

        error = getError(jqXHR,exception);
        $('#titleModalError').html("OOps!!, algo salio mal ⛔️ ");
        $('.modal-body').html(
            "<p>" + error.msg + "</p>" + 
            "<p>Código de Error: " + error.code +  "</p>" 
        );
        $('#modalError').modal('show');
    }


    $("#getDocumentButton").on('click', function () {
        /**
         * Send an ajax request to download the file just created on the server. 
         * Due to type conflicts, if the file is json, its request must be evaluated separately
         */
        
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
                    createModalError(jqXHR,exception);
                    $('.file_upload').prop('disabled', false);
                    $("#getDocumentButton").hide();
                }
            });
    
        }
    });


    $("#getUrlButton").on('click', function () {
        /**
         * Send an ajax request to download the html file just created on the server. 
         * Due to type conflicts, if the file is json, csv or html, its request must be evaluated separately
         */

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
                    createModalError(jqXHR,exception);
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
                    createModalError(jqXHR,exception);
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
                    createModalError(jqXHR,exception);
                    $('#html_upload').prop('disabled', false);
                    $("#getUrlButton").hide();
                }
            });
        }
    });


    $("#formId").submit(function(e) {
        // Send an ajax request to analyze the sent document.

        e.preventDefault(); 
    
        if (!checkFileExtension()) {
            return;
        }

        let personalData = getTypeOfPersonalData();
        if (personalData == null) {
            $('#alert').text("* Elige uno de los tipos de datos presentados");
            return;
        } else {
            $('#alert').text("");
        }

        $("#spinner").show();
        $('.file_upload').prop('disabled', true);

        let url  = getUrlServer(personalData);
        let formData = new FormData(this);
    
        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            success: function(data)
            {
                id = data.id;
                fileType = data.fileType;
                $("#getDocumentButton").show();
                $("#spinner").hide();
            },
            error: function(jqXHR,exception){
                createModalError(jqXHR,exception);
                $("#spinner").hide();
                $('.file_upload').prop('disabled', false);
            },
            cache: false,
            contentType: false,
            processData: false
        });

    });


    $("#form_web").submit(function(e) {
        // Send an ajax request to analyze the html document sent.

        e.preventDefault(); 
        if (!validateUrlForm()) {
            return;
        }

        let personalData = getTypeOfPersonalData();
        if (personalData == null) {
            $('#alert').text("* Elige uno de los tipos de datos presentados");
            return;
        } else {
            $('#alert').text("");
        }

        $("#spinner_web").show();
        $('#html_upload').prop('disabled', true);

        let url  = server + '/search/file/operation-web?url=' +
        $("#url_web").val() + "&op=" + $("#op").val() + "&personalData=" + personalData;
        $.ajax({
            type: "GET",
            url: url,
            success: function(data)
            {
                idUrl = data.id;
                fileTypeUrl = data.fileType;
                $("#getUrlButton").show();
                $("#spinner_web").hide();
            },
            error: function(jqXHR,exception){
                createModalError(jqXHR,exception);
                $("#spinner_web").hide();
                $('#html_upload').prop('disabled', false);
            }
        });
    });

});

function validateUrlForm() {
    /**
     * Validate the form to send web pages
     */
    
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
    /**
     * Analyzes the extension of the file
     */

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
    /**
     * Analyzes the error in the request
     * returns error code and message
     */
    
    let error = {"code":-1, "msg":""} ;
    if (jqXHR.status === 0) {
        error.msg = 'No estas concetado al servidor.\nVerifica tu conexión.';
    } else if (jqXHR.status == 404) {
        error.msg = 'Petición no procesada. [404]';
    } else if (jqXHR.status == 500) {
        error.msg = 'Error en servidor interno [500].';
    } else if (exception === 'parsererror') {
        error.msg = 'El análisis JSON solicitado ha fallado.';
    } else if (exception === 'timeout') {
        error.msg = 'Error de tiempo de espera.';
    } else if (exception === 'abort') {
        error.msg = 'Solicitud abortada.';
    } else {
        error.msg = 'Error no detectado.Vuelva ha intentarlo.';
    }
    error.code = jqXHR.status;
    return error;
}

