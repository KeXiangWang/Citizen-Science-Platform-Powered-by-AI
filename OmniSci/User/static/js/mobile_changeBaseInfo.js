/*
* 修改基本个人信息，包括：
* 头像
* 自我介绍
* 邮箱
* 性别
* 年龄
*
* 需要手写格式检查以及判断信息是否发生了变化
* */

layerData = new FormData();


$(document).ready(function () {
    $('.editable').on('click', function () {
        var that = $(this);
        if (that.find('input').length > 0 || that.find('textarea').length) {
            return;
        }
        var currentText = that.text();

        // console.log(that[0].id);
        var $input;
        if (that[0].id == 'description') {
            $input = $('<textarea>').val(currentText)
        } else {
            $input = $('<input>').val(currentText)
            $input.css({
                height: that.height(),
            })
        }

        $input.css({
            position: 'absolute',
            top: '0px',
            left: '0px',
            width: that.width(),
            opacity: 0.9,
            padding: '10px'
        });

        $(this).append($input);

        that.mouseleave(function () {
            if ($input.val()) {
                that.text($input.val());
            }
            that.find('input').remove();
            that.find('text').remove();
        });
        // Handle outside click
        $(document).click(function (event) {
            if (!$(event.target).closest('.editable').length) {
                if ($input.val()) {
                    that.text($input.val());
                }
                that.find('input').remove();
                that.find('text').remove();
            }
        });
    });
});

// //打开上传头像层
// const upload_avatar = () => {
//     layerData = new FormData();
//     layer.open({
//         area: [window.innerWidth + 'px', window.innerHeight + 'px'],
//         title: "",
//         type: 2,                             //0:信息框;1:页面层;2:iframe层;3:加载层;4:tips层
//         content: "/user/avatar/",
//     });
// }

$('#change-avatar').on('change', function(){
    var filePath = $(this).val();
    var fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase();
    var src = window.URL.createObjectURL(this.files[0]);

    // if( !fileFormat.match(/.png|.jpg|.jpeg/) ) {
    //     error_prompt_alert('Wrong format, the file must end with png, jpg or jpeg');
    //     return;
    // }
    layerData.append("image",this.files[0],'avatar.png');
    $('#avatar-preview').attr('src',src);
});

//邮箱格式检查
const valid_email = () => {
    const email = $('#email').text();
    // console.log('email',email);
    const reg = new RegExp("^[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+){0,4}$");
    return (reg.test(email) || email == 'Secret' || email == 'secret');
}

//年龄格式检查
const valid_age = () => {
    const age = $('#age').text();
    const reg = new RegExp("^[0-9]{1,2}$");
    return (reg.test(age) || age == 'Secret' || age == 'secret');
}


