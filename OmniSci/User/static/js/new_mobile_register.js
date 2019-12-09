let step = 0;           //表示到第几步了（0-3）
let code = "default";          //验证码
let registerData = new FormData();      //全部注册信息

const hide_feedback = () => {
    // $('.invalid-feedback').fadeOut("slow");
    $('input').removeClass('is-invalid');
    $('#email-box > div')[0].innerText = '请输入正确的邮箱地址';
}

hide_feedback();
$('#back-btn').hide();

$('#back-btn').click(function () {
    console.log('click');
    if (step > 0) {
        $('#step-' + step.toString()).fadeOut("slow");
        $('#bar-' + step.toString()).fadeOut("slow");
        step -= 1;
        $('#step-' + step.toString()).fadeIn("slow");
        $('#bar-' + step.toString()).fadeIn("slow");
    }
    if (step==0){
        $('#back-btn').hide();
    }
})

function checkForm(str, regex) {
    if (str == null || str == "") return false;
    return regex.test(str);
}

const validCheck_0 = () => {

    //检查邮箱有效性
    let email_regex = /(^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$)/;
    let email_input = $("input[name='c_email']").val();

    //检查用户名有效性
    let user_regex = /(^[\u4e00-\u9fa5a-zA-Z_0-9]{1,14}$)/;
    let user_input = $("input[name='c_name']").val();

    if (!checkForm(user_input, user_regex)) {
        // $('#username-feedback').fadeIn("slow");
        console.log('hit');
        $('#username').addClass('is-invalid');
        return false;
    }

    if (!checkForm(email_input, email_regex)) {
        $('#email').addClass('is-invalid');
        return false;
    }

    return true;
}

const validCheck_1 = () => {
    let pwd_regex = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_]+$)(?![a-z0-9]+$)(?![a-z\W_]+$)(?![0-9\W_]+$)[a-zA-Z0-9\W_]{8,16}$/;
    let pwd_input = $("input[name='c_pwd']").val();
    let pwd2_input = $("input[name='c_pwd2']").val();

    console.log('pwd',pwd_input);
    if (!checkForm(pwd_input, pwd_regex)) {
        // $('#pwd-feedback').fadeIn("slow");
        $('#password').addClass('is-invalid');
        return false;
    }

    if (pwd_input != pwd2_input) {
        // $('#check-pwd-feedback').fadeIn("slow");
        $('#check_password').addClass('is-invalid');
        return false;
    }

    return true;
}

const validCheck_2 = ()=>{
    let age_regex = /^[0-9]{1,2}$/;
    let age_input = $("input[name='age']").val();

    console.log(age_input);
    if (age_input!="" && !checkForm(age_input, age_regex)) {
        // $('#age-feedback').fadeIn("slow");
        $('#age').addClass('is-invalid');
        return false;
    }

    return true;
}



const next_step = () => {
    $('#step-' + step.toString()).fadeOut("slow");
    $('#bar-' + step.toString()).fadeOut("slow");
    step += 1;
    $('#step-' + step.toString()).fadeIn("slow");
    $('#bar-' + step.toString()).fadeIn("slow");
}

// next_step();
// next_step();
// next_step();

$('#finish-step0').click(function () {
    $('#back-btn').fadeIn();
    hide_feedback();
    if (validCheck_0()) {
        const code_input = $("input[name='auth']").val();
        if (code_input != code) {
            // alert(code_input + " " + code);
            $('#code-feedback').fadeIn("slow");
        } else {
            registerData.append('c_name', $("input[name='c_name']").val());
            registerData.append('c_email', $("input[name='c_email']").val());
            registerData.append('auth', $("input[name='auth']").val());

            next_step();

        }
    }
})

$('#finish-step1').click(function () {

    hide_feedback();
    if(validCheck_1()){
        registerData.append('c_pwd', $("input[name='c_pwd']").val());
        registerData.append('c_pwd2', $("input[name='c_pwd2']").val());

        console.log(registerData.get('c_pwd'));
        next_step();
    }
})

$('#finish-step2').click(function () {

    hide_feedback();
    if(validCheck_2()){
        registerData.append('sex', $('input:radio[name="sex"]:checked').val());
        registerData.append('age', $("input[name='age']").val());
        //自我介绍先置为空了
        registerData.append('q_msg', '');
        next_step();
    }
})


$('#avatar-upload').click(function () {
    $('#avatar-input').trigger('click');
})

$('#avatar-input').on('change',function () {
    var filePath = $(this).val();
    var fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase();
    var src = window.URL.createObjectURL(this.files[0]);
    if( !fileFormat.match(/.png|.jpg|.jpeg/) ) {
        // $('#avatar-feedback').fadeIn("slow");
        $('#avatar-input').addClass('is-invalid');
        return;
    }
    registerData.append("image",this.files[0],'avatar.png');
    $('#avatar-preview').attr('src',src);
    $('#avatar-preview').removeClass('upload');
    $('#avatar-preview').addClass('rounded-circle');
    $('#avatar-preview').addClass('preview');
    // $('#avatar-box').fadeIn("slow");
})