
function alert(text)
{
    var popup = '<div id="popup-alert" class="popup row justify-content-center m-0 rounded-50" style="display: none;"><div class="popup-info col-auto rounded">' + text + '</div></div>'
    $('body').append(popup);
    $('#popup-alert').fadeIn();
    setTimeout(function () {
        $('#popup-alert').fadeOut(function () {
            $(this).remove();
        });
    }, 1500);
}

function confirm(text, confirm, cancel)
{
    var overlay = document.getElementById('page-overlay-confirm');
    overlay.style['display'] = 'block';
    var popup =
        '<div id="popup-confirm" class="popup row justify-content-center m-0">\n' +
        '    <div class="popup-dialogue col-8">\n' +
        '        <div class="row m-0">\n' +
        '            <div class="col-auto pl-0">\n' +
        '                <i class="text-theme fa fa-question"></i>\n' +
        '            </div>\n' +
        '            <div class="col pl-0">\n' +
        '                <span class="text-muted">' + text + '</span>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '        <div class="row m-0 mt-1">\n' +
        '            <button id="cancel" class="col btn btn-focus-0 bg-white border-top border-right  text-muted">取消</button>\n' +
        '            <button id="confirm" class="col btn btn-focus-0 bg-white border-top text-theme">确认</button>\n' +
        '        </div>\n' +
        '    </div>\n' +
        '</div>';
    $('body').append(popup);
    $('#confirm').on('click', function(){
        $('#popup-confirm').remove();
        overlay.style['display'] = 'none';
        confirm();
    });
    $('#cancel').on('click', function(){
        $('#popup-confirm').remove();
        overlay.style['display'] = 'none';
        cancel();
    });
}