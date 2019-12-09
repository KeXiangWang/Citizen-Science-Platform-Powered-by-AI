/**
 * @method userJoin
 * @desc 上传用户参与请求，给出反馈信息
 */
function userJoin(is_mobile)
{
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
        url: "/project/join/" + pid + "/",
        success: function (msg) {
            if (msg.result) {
                var btn = document.querySelector('#user-join');

                if(is_mobile){
                    btn.classList.remove('btn-theme');
                    btn.classList.add('inactive-btn');
                    document.querySelector('#user-join > small').innerHTML = '<i class="fa fa-users" aria-hidden="true"></i>&nbsp;已参加';

                    $(btn).css("pointer-events","none");
                }
                else {
                    btn.classList.remove('normal-btn');
                    btn.classList.add('inactive-btn');
                    btn.innerHTML = '<i class="fa fa-users"></i>&nbsp;已参加';

                    $(btn).addClass("focus").css("pointer-events", "none");
                }
                alert(msg.msg);
            } else {
                alert('Participate unsuccessfully ' + msg.msg);
            }
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

function userBadDataOption(data_id, option) {
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {
            "csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val(),
            "data_id": data_id,
            "option": option
        },
        url: "/project/bad_submit/",
        success: function (msg) {
            if (!msg.result) {
                alert('Operate unsuccessfully ' + msg.msg);
            }
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

/**
 * @method userBadData
 * @param data_id 数据id
 * @param info 提醒信息
 * @param is_mobile
 * @desc AI判断类型错误，请用户重新确认
 */
function userBadData(data_id, info, is_mobile) {
    if (is_mobile) {
        confirm(info, function(){
            alert('Submit successfully');
            var img = $('#user-upload-img');
            img.attr('src', '/static/images/svg/add.svg');
            img.attr('class', 'p-0');
            img.attr('style', 'width: 20%; height: 20%; margin-top: 38%; object-fit: fill;');
            userBadDataOption(data_id, 'confirm');
        }, function(){
            userBadDataOption(data_id, 'remove');
        });
        return;
    }
    if (confirm(info)) {
        userBadDataOption(data_id, 'confirm');
        alert('Submit successfully');
        $('#user-upload-img').attr('src', '');
        document.querySelector('#user-submit').value = '';
    } else {
        userBadDataOption(data_id, 'remove');
    }
}

/**
 * @method userSubmit
 * @param is_mobile boolean 是否是手机端
 * @desc 上传用户提交请求，给出反馈信息
 */
function userSubmit(is_mobile)
{
    var formData = new FormData();
    var select = document.querySelector('#img-label');
    var province = document.querySelector('#province');
    var city = document.querySelector('#city');
    var submit = document.querySelector("#submit-btn");

    $(submit).css("pointer-events", "none");

    formData.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());

    if (is_mobile) {
        formData.append('image', $('#img-upload-btn')[0].files[0]);
    } else {
        formData.append('image', $('#user-submit')[0].files[0]);
    }

    if (select && select.options[select.selectedIndex]) {
        formData.append('label', select.options[select.selectedIndex].text)
    }

    if (province) {
        formData.append('province', province.options[province.selectedIndex].text)
    }

    if (city) {
        formData.append('city', city.options[city.selectedIndex].text)
    }

    $.ajax({
        type: "POST",
        datatype: "json",
        data: formData,
        cache: false,
        processData : false,
        contentType : false,
        async: false,
        url: "/project/submit/" + pid + "/",
        success: function (msg) {
            if (msg.result) {
                alert(msg.msg);
                var img = $('#user-upload-img');
                if (is_mobile) {
                    img.attr('src', '/static/images/svg/add.svg');
                    img.attr('class', 'p-0');
                    img.attr('style', 'width: 20%; height: 20%; margin-top: 38%; object-fit: fill;');
                } else {
                    img.attr('src', '');
                    document.querySelector('#user-submit').value = '';
                }
            } else {
                if (msg.msg == 'Bad data') {
                    userBadData(msg.data_id, 'AI rejects the image, please check it', is_mobile);
                } else if (msg.msg == 'Low reputation') {
                    userBadData(msg.data_id, 'Low reputation, please confirm it', is_mobile);
                } else {
                    alert('Submit unsuccessfully ' + msg.msg);
                }
            }
            $(submit).css("pointer-events", "auto");
        },
        error : function(msg) {
            alert(msg);
            window.location.reload();
        }
    });
}

function auditedSwitch(flag)
{
    if (audition == flag) {
        return;
    }
    document.querySelector('#info-content-divider > div:nth-child(2)').style.visibility = 'hidden';
    audition = flag;
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
        },
        url: "/project/detail_page_cnt/" + pid + "/" + (audition ? 1 : 2) +"/",
        success: function (data) {
            page_cnt = data.page_cnt;

            for (var i = 1;i <= 9;i ++) {
                if (audition) {
                    document.querySelector('#accepted_' + i).style.display = 'block';
                    document.querySelector('#declined_' + i).style.display = 'none';
                } else {
                    document.querySelector('#accepted_' + i).style.display = 'none';
                    document.querySelector('#declined_' + i).style.display = 'block';
                }
            }

            if (audition) {
                verified = 1;
                document.querySelector('#audited-accept-all').style.display = 'block';
                document.querySelector('#audited-decline-all').style.display = 'none';
                document.querySelector('#audited > div:nth-child(1) > a').classList.add('choosed-btn');
                document.querySelector('#audited > div:nth-child(2) > a').classList.remove('choosed-btn');
            } else {
                verified = 2;
                document.querySelector('#audited-accept-all').style.display = 'none';
                document.querySelector('#audited-decline-all').style.display = 'block';
                document.querySelector('#audited > div:nth-child(1) > a').classList.remove('choosed-btn');
                document.querySelector('#audited > div:nth-child(2) > a').classList.add('choosed-btn');
            }

            createData();
            document.querySelector('#info-content-divider > div:nth-child(2)').style.visibility = 'visible';
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

/**
 * @method userAudition
 * @param data_id int
 * @param option str accept | decline | delete
 * @desc 用户处理图片
 */
function userAudition(data_id, option)
{
    $.ajax({
        type: "POST",
        datatype: "json",
        url: "/project/audition/" + pid + "/",
        data: {
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
            'data_id': data_id,
            'verified': verified,
            'option': option
        },
        success: function (data) {
            if (!data.result) {
                alert(data.msg);
                return;
            }
            page_cnt = data.page_cnt;
            now_page = now_page > page_cnt ? page_cnt : now_page;
            var page = document.querySelector('#project-data-page > div');
            if (page_cnt > 9)
            {
                if (now_page + 4 > page_cnt) {
                    createPage(page.children[0], page_cnt - 8, page_cnt, 'changePage', now_page);
                } else if (now_page - 4 < 1) {
                    createPage(page.children[0],1, 9, 'changePage', now_page);
                } else {
                    createPage(page.children[0],now_page - 4, now_page + 4, 'changePage', now_page);
                }
            } else {
                if (page_cnt <= 1) {
                    page.style.display = 'none';
                } else {
                    page.style.display = 'block';
                    createPage(page.children[0],1, page_cnt, 'changePage', now_page);
                }
            }

            writeData(now_page);
            alert("Deal successfully");
        },
        error: function (msg) {
            alert(msg);
        }
    });
}

/**
 * @method userAuditionAll
 * @param option str accept | decline | delete
 * @desc 用户处理图片
 */
function userAuditionAll(option)
{
    $.ajax({
        type: "POST",
        datatype: "json",
        url: "/project/audition_all/" + pid + "/",
        data: {
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
            'verified': verified,
            'option': option
        },
        success: function (data) {
            if (!data.result) {
                alert(data.msg);
                return;
            }
            page_cnt = data.page_cnt;
            now_page = now_page > page_cnt ? page_cnt : now_page;
            var page = document.querySelector('#project-data-page > div');
            if (page_cnt > 9)
            {
                if (now_page + 4 > page_cnt) {
                    createPage(page.children[0], page_cnt - 8, page_cnt, 'changePage', now_page);
                } else if (now_page - 4 < 1) {
                    createPage(page.children[0],1, 9, 'changePage', now_page);
                } else {
                    createPage(page.children[0],now_page - 4, now_page + 4, 'changePage', now_page);
                }
            } else {
                if (page_cnt <= 1) {
                    page.style.display = 'none';
                } else {
                    page.style.display = 'block';
                    createPage(page.children[0],1, page_cnt, 'changePage', now_page);
                }
            }

            writeData(now_page);
            alert("Deal successfully");
        },
        error: function (msg) {
            alert(msg);
        }
    });
}

/**
 * @method userResponse
 * @desc 上传用户评论请求，给出反馈信息
 */
function userResponse()
{
    var content = document.querySelector("#editormd > div.CodeMirror.cm-s-default.CodeMirror-wrap >" +
        " div.CodeMirror-scroll > div.CodeMirror-sizer > div > div > div > div.CodeMirror-code");

    var line_num = content.children.length;

    if (content.innerText.length - line_num > 100) {
        alert('Too long response');
        return;
    }

    var formData = new FormData();
    var markdown = document.querySelector('#editormd > div.editormd-preview > div');
    formData.append('content', markdown.innerHTML);
    formData.append('preview', content.innerText);
    formData.append('line', line_num);
    formData.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());
    $.ajax({
        type: "POST",
        datatype: "json",
        data: formData,
        cache: false,
        processData : false,
        contentType : false,
        async: false,
        url: "/project/response/" + pid + "/" + now_issue_id + "/",
        success: function (msg) {
            if (msg.result) {
                alert(msg.msg);
                comment_page_cnt = msg.comment_page_cnt;
                changeCommentPage(comment_page_cnt, false);
                writeComment(comment_page_cnt);
                var page = document.querySelector('#post-detail > div:nth-child(7) > div.row > div > div');
                if (comment_page_cnt <= 1) {
                    page.style.display = 'none';
                } else {
                    page.style.display = 'block';
                    createPage(page, Math.max(comment_page_cnt - 9, 1), comment_page_cnt,
                        'changeCommentPage', comment_page_cnt);
                }
            } else {
                alert('Response unsuccessfully ' + msg.msg);
            }
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

/**
 * @method userAddPost
 * @desc 上传用户提问请求，给出反馈信息
 */
function userAddPost()
{
    var title = document.querySelector('#add-post > div:nth-child(2) > div:nth-child(1) > input[type="text"]');
    var description = document.querySelector('#add-post > div:nth-child(2) > div:nth-child(2) > input[type="text"]');

    if (title.value.length > 100) {
        alert('Too long issue title');
        return;
    }

    if (description.value.length > 280) {
        alert('Too long issue description');
        return;
    }

    var formData = new FormData();

    formData.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());
    formData.append("title", title.value);
    formData.append("description", description.value);
    $.ajax({
        type: "POST",
        datatype: "json",
        data: formData,
        cache: false,
        processData : false,
        contentType : false,
        async: false,
        url: "/project/addPost/" + pid + "/",
        success: function (msg) {
            if (msg.result) {
                alert(msg.msg);
                window.location.reload();
            } else {
                alert('Add post unsuccessfully ' + msg.msg);
            }
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

/**
 * @method userAddAuthority
 * @desc 用户增加协助志愿者
 */
function userAddAuthority()
{
    var mail = document.querySelector('#grant-email').value;
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
            'mail': mail
        },
        url: "/project/addAuthority/" + pid + "/",
        success: function (msg) {
            if (msg.result) {
                alert(msg.msg);
                var container = document.createElement('div');
                container.classList.add('row', 'info-row');
                container.innerHTML =
                    "<div class=\"col-md-4\">" + msg.user['user_name'] + "</div>" +
                    "<div class=\"col-md-4\">" + msg.user['email_address'] + "</div>" +
                    "<div class=\"col-md-4 cancel-grant\">" +
                    "    <a href=\"javascript:void(0)\" onclick=\"userRemoveAuthority(" + msg.user['uid'] +", this)\">取消授权</a>" +
                    "</div>";

                var last = document.querySelector('#add-assistant')
                var parent = last.parentNode;
                parent.insertBefore(container, last);
            } else {
                alert('Add unsuccessfully ' + msg.msg);
            }
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

/**
 * @method userAddAuthority
 * @param uid
 * @param element
 * @desc 用户删除协助志愿者
 */
function userRemoveAuthority(uid, element)
{
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
            'uid': uid
        },
        url: "/project/removeAuthority/" + pid + "/",
        success: function (msg) {
            if (msg.result) {
                alert(msg.msg);
                var container = element.parentNode.parentNode;
                container.parentNode.removeChild(container);
            } else {
                alert('Remove unsuccessfully ' + msg.msg);
            }
        },
        error : function(msg) {
            alert(msg);
        }
    });
}