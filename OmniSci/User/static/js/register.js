let layerData = new FormData();
let code = "default";

//检查验证码是否正确
const codeCheck = ()=>{
    const code_input = $("input[name='auth']").val();
    return (code_input==code);
}

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

//打开上传头像层
const upload_avatar = () => {
    layerData = new FormData();
    layer.open({
        area: [window.innerWidth+'px', window.innerHeight+'px'],
        title: "上传头像",
        type: 2,                             //0:信息框;1:页面层;2:iframe层;3:加载层;4:tips层
        content: "/user/avatar/",
    });
}


