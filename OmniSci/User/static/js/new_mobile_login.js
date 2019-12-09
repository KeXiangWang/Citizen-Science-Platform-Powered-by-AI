function checkForm(str,regex) {
    if (str == null || str == "") return false;
    return regex.test(str);
}

$('#submit-btn').click(function () {
    user_or_email = /(^[\u4e00-\u9fa5a-zA-Z_0-9]{1,14}$)|(^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$)/;
    pwd = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_]+$)(?![a-z0-9]+$)(?![a-z\W_]+$)(?![0-9\W_]+$)[a-zA-Z0-9\W_]{8,16}$/;

    user_input = $("input[name='c_name']").val();
    pwd_input = $("input[name='c_pwd']").val();

    //初始状态，全部隐藏feedback
    $('#username-feedback').hide();
    $('#pwd-feedback').hide();

    console.log('clicked');
    if(!checkForm(user_input,user_or_email)){
         $('#username-feedback').fadeIn("slow");
    }else if(!checkForm(pwd_input,pwd)){
        $('#pwd-feedback').fadeIn("slow");
    }else{
        $('#login-form').trigger('submit');
    }
})