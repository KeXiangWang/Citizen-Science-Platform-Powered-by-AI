var layerData = new FormData();

//检查两次输入的密码是否一致
const pwdCheck = () => {

    const pwd1 = document.getElementsByName("c_pwd")[0].value;
    const pwd2 = document.getElementsByName("c_pwd2")[0].value;
    // console.log('pwd', pwd1, pwd2);
    if (pwd1 != pwd2) {
        alert("两次输入的密码不一致!");
    }
    return (pwd1 == pwd2);
}

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
    $('#avatar-preview').show();
    // console.log('avatar',$('#avatar-preview').style.display);
});


