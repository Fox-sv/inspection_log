$(document).ready(function(){

function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}

    $('#preloader').hide();
    $('#file').bind('change', function(){
    var data = new FormData();
var error = '';
    jQuery.each($('#file')[0].files, function(i, file) {

            if(file.name.length < 1) {
                error = error + ' Файл имеет неправильный размер! ';
            }
            if(file.size > 1000000) {
                error = error + ' File ' + file.name + ' is to big.';
            }
            if(file.type != 'image/png' && file.type != 'image/jpg' && !file.type != 'image/gif' && file.type != 'image/jpeg' ) {
                error = error + 'File  ' + file.name + '  doesnt match png, jpg or gif';
            }

        data.append('file-'+i, file);

    });

if (error != '') {$('#info').html(error);} else {

        $.ajax({
            url: 'ALARM_URL',
            type: 'POST',
                xhr: function() {
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload){ // проверка что осуществляется upload
                    myXhr.upload.addEventListener('progress',progressHandlingFunction, false); //передача в функцию значений
                }
                return myXhr;
                },
            data: data,
            cache: false,
            contentType: false,
            processData: false,

            beforeSend: function() {
              $('#preloader').show();
            },

            success: function(data){
                $('#info').html(data);
                $('#preloader').hide();

            }

            ,
            error: errorHandler = function() {
                $('#info').html('Ошибка загрузки файлов');
            }

        });

        }
    })

});