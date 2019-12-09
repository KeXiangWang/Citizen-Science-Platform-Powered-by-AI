/**
 * @method
 * @desc 即时显示用户上传的缩略图
 *      1. 获取图片位置，转化为课显示url
 *      2. 判断图片格式，返回错误
 *      3. 显示图片
 */
$('#choose-image').on('change', function(){
    var filePath = $(this).val();
    var fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase();
    var src = window.URL.createObjectURL(this.files[0]);

    if( !fileFormat.match(/.png|.jpg|.jpeg/) ) {
        error_prompt_alert('Wrong format, the file must end with png, jpg or jpeg');
        return;
    }

    $('#project-image').attr('src',src);
});


function valid()
{
    var name = document.querySelector('#project-name').value;
    var introduction = document.querySelector('#project-intro').value;
    var label = document.querySelector('#project-label').value;
    var model = document.querySelector('#user-defined-ai').value;

    if (name.length > 30) {
        alert('Too long project name');
        return false;
    }

    if (introduction.length > 2000) {
        alert('Too long project introduction');
        return false;
    }

    if (label.length > 2000) {
        alert('Too long project label');
        return false;
    }

    if (model.length > 200) {
        alert('Too long project model');
        return false;
    }

    return true;
}