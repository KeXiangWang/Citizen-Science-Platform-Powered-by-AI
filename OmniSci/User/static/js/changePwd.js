//检查两次输入的密码是否一致
const pwdCheck = () => {
    const pwd1 = document.getElementsByName("new_pwd")[0].value;
    const pwd2 = document.getElementsByName("repeat_pwd")[0].value;
    // console.log('pwd', pwd1, pwd2);
    if (pwd1 != pwd2) {
        alert('两次输入的密码不一致!');
    }
    return (pwd1 == pwd2);
}