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
            case "4":
                $('#formId').attr('action', server+'/search/file/tagger-html');
                break;
            case "5":
                $('#formId').attr('action', server+'/search/file/disintegration');
                break;
            case "6":
                $('#formId').attr('action', server+'/search/file/obfuscation');
                break;
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

    let id = '04363f5c-4c91-4c9a-9204-27a1e190d183'
    $("#getDocumentButton").on('click', function () {
        $("#getDocument").attr("action", server+'/search/file/download?id=' + id);
        /*var element = document.createElement('a');
        element.setAttribute('href', server+'/search/file/download?id=' + id);
        //element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);
        try {
            element.click();
        } catch (error) {
            console.error(error);
        }
        document.body.removeChild(element);*/
        /*fetch(server + '/search/file/download?id=' + id)
            .then(resp => resp.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                // the filename you want
                a.download = 'doc.txt';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                //alert('your file has downloaded!'); // or you know, something with better UX...

            })
            .catch((error) => alert(error));*/
        /*$.get(server+'/search/file/download',
        {
            id: id
        },
        function(data, status){
            alert("Data: " + data + "\nStatus: " + status);
        });*/
        $.ajax({
            url: server+'/search/file/download?id='+id,
            type: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function(data){ 
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = 'myfile.txt';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            },
            error: function(data) {
                alert('woops!'); //or whatever
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

