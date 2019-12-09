
window.onload = function(){
    $.ajax({
        url: '/user/brief-profile/',
        type: 'POST',
        datatype:'json',
        data: {"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
        success: function (msg) {
            msg = JSON.parse(msg);

            if (msg['logged_in']) {

                $("#login-btn").attr("style","display:none");
                $("#user-profile-btn").attr("style","display:block");
                $(".user-brief-profile span").text(msg['u_name']);
                // for(var i = 0; i<user_profile_list.length;git lo i+=1){
                //     user_profile_list[i].innerHTML = user_profile_list[i].innerHTML + msg['u_name'];
                // }
                $("#user-profile-img").attr('src', msg['avatar_path']);

            } else {
                $("#user-profile-btn").attr("style","display:none");
            }
        },
        error(msg){
            alert(msg);
        }
    })
};

function changeMode() {
    var origin_url = window.location.href;

     $.ajax({
        url: '/user/change-mode/',
        type: 'POST',
        datatype:'json',
        async: false,
        data: {"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
        success: function (msg) {
            window.location.href = origin_url;
            window.location.reload();
        },
        error: function (msg) {
            window.alert(msg);
        }
     })
}
