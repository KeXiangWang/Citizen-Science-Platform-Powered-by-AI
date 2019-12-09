
window.onload = function(){
    $.ajax({
        url: '/user/brief-profile/',
        type: 'POST',
        datatype:'json',
        data: {"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
        success: function (msg) {
            msg = JSON.parse(msg);
            if (msg['logged_in']) {
                $("#avatar").attr('src', msg['avatar_path']);
                $("#user_name").text(msg['u_name']);
                $("#avatar").parent().attr('href', '/user/profile/');
                $("#user_name").parent().attr('href', '/user/profile/');
                var user_info = document.getElementById('user_info');
                if (msg['release']) {
                    user_info.innerHTML += '<small class="badge badge-theme">志愿者</small>\n';
                }
                if (msg['volunteer']) {
                    user_info.innerHTML += '<small class="badge badge-primary">发布者</small>\n';
                }
                user_info.innerHTML += '<small class="badge badge-warning">信誉: ' + msg['credit'] + '</small>'
            } else {
                window.location.href = '/user/login/';
            }
        },
        error(msg){
            alert(msg);
        }
    })
};