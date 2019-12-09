/**
 * @method writePost
 * @param page_num int post页数
 * @desc 创建所有post
 */
function writePost(page_num)
{
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
        url: "/project/forum_page/" + pid + "/" + page_num + "/",
        success: function (data) {
            var issue = data.issue;
            var i, num = issue.length;

            for (i = 5;i >= 1;i --)
            {
                var container = document.querySelector('#project-discussion > div:nth-child(' + i + ')');

                var title = document.querySelector('#project-discussion > div:nth-child(' + i + ') >' +
                    ' div.col-md-11 > a > h4');

                var description = document.querySelector('#project-discussion > div:nth-child(' + i + ') >' +
                    ' div.col-md-11 > p');

                if (i <= num) {
                    container.style.display = 'block';

                    title.innerHTML = issue[i - 1]['title'];

                    $(title).attr('onclick', 'jumpPost(' + issue[i - 1]['issue_id'] +')');

                    description.innerHTML = issue[i - 1]['description'];

                } else {
                    container.style.display = 'none';
                }
            }
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

/**
 * @method createPost
 * @desc 完成数据填充
 *      1. 创建换页框
 *      2. 填充数据
 */
function createPost()
{
    var i;
    var page = document.querySelector('#project-discussion > div:nth-child(6) > div > div');

    // 处理换页框
    if (issue_page_cnt <= 1) {
        page.style.display = 'none';
    } else {
        page.style.display = 'block';
        createPage(page, 1, Math.min(issue_page_cnt, 9), 'changePostPage', 1);
    }

    // 写入第一页数据
    writePost(1);
}

var now_post_page = 1;
/**
 * @method changePostPage
 * @param next_page
 * @param flag
 * @desc 切换项目数据页面
 *      1. 判断按钮性质，计算目标页码
 *      2. 判断目标页码合理性，换页
 */
function changePostPage(next_page, flag)
{
    var page = document.querySelector('#project-discussion > div:nth-child(6) > div > div');

    if (flag) {
        next_page = next_page + now_post_page;
    }

    if (next_page >= 1 && next_page <= issue_page_cnt) {
        now_post_page = next_page;
        writePost(now_post_page);
        if (issue_page_cnt > 9) {
            if (now_post_page + 4 > issue_page_cnt) {
                createPage(page, issue_page_cnt - 8, issue_page_cnt, 'changePostPage', now_post_page);
            } else if (now_post_page - 4 < 1) {
                createPage(page,1, 9, 'changePostPage', now_post_page);
            } else {
                createPage(page,now_post_page - 4, now_post_page + 4, 'changePostPage', now_post_page);
            }
        } else {
            createPage(page,1, issue_page_cnt, 'changePostPage', now_post_page);
        }
    }
}

var comment_page_cnt;
var now_issue;
var now_issue_id = 0;
/**
 * @method jumpPost
 * @param issue_id int issue的id
 * @desc
 */
function jumpPost(issue_id)
{
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
        url: "/project/forum/" + issue_id + "/",
        success: function (data) {
            // 获取数据
            comment_page_cnt = data.comment_page_cnt;
            now_issue = data.issue;
            now_issue_id = issue_id;

            // 显示详细内容
            document.querySelector('#post-list').classList.remove('show');
            document.querySelector('#post-list').classList.add('hidden');
            document.querySelector('#post-detail').classList.remove('hidden');
            document.querySelector('#post-detail').classList.add('show');

            // 渲染markdown编辑器
            $(function() {
                var testEditor = editormd("editormd", {
                    width   : "100%",
                    height  : 450,
                    // syncScrolling : "single",
                    path    : "/static/lib/",
                    placeholder : "Ask anything!",
                    tex: false,
                    emoji: false,
                    taskList: false,
                    toolbar: false
                });
            });

            now_comment_page = 1;
            min_comment_page = 0;

            // 渲染post内容
            createComment();
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

/**
 * @method writeComment
 * @param page_num int comment页数
 * @desc 写入comment内容
 */
function writeComment(page_num)
{
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
        url: "/project/comment_page/" + now_issue_id + "/" + page_num + "/",
        success: function (data) {
            var comments = data.comment;
            var i, num = comments.length;

            for (i = 5;i >= 1;i --)
            {
                var container = document.querySelector('#response_' + i);

                var user = document.querySelector("#response_" + i + " > div.clear-sides-10.response-owner > h5");

                var number = document.querySelector("#response_" + i + " > div.clear-sides-10.response-owner > span");

                var text = document.querySelector("#response_" + i + " > div.clear-sides-10.response-text");

                if (i <= num) {
                    container.style.display = 'block';

                    user.innerHTML = comments[i - 1]['user_name'];

                    number.innerHTML = ((page_num - 1) * 5 + i) + '楼';

                    text.innerHTML = comments[i - 1]['text'];

                } else {
                    container.style.display = 'none';
                }
            }
        },
        error : function(msg) {
            alert(msg);
        }
    });
}

/**
 * @method createComment
 * @desc 修改issue的信息，创建页框
 */
function createComment()
{
    var title = document.querySelector('#post-title > h4');
    var user = document.querySelector('#post-owner > span > span:nth-child(1) > b');
    var time = document.querySelector('#post-owner > span > span.clear-sides-30');
    var description = document.querySelector('#ISSUE_ID-description');
    title.innerHTML = now_issue['title'];
    user.innerHTML = now_issue['user_name'];
    time.innerHTML = now_issue['time'];
    description.innerHTML = now_issue['description'];

    var i;
    var page = document.querySelector('#post-detail > div:nth-child(7) > div.row > div');

    // 处理换页框
    if (comment_page_cnt <= 1) {
        page.style.display = 'none';
    } else {
        page.style.display = 'block';
        createPage(page.children[0], 1, Math.min(comment_page_cnt, 9), 'changeCommentPage', 1);
    }

    // 写入第一页数据
    writeComment(1);
}


var now_comment_page = 1;
/**
 * @method changeCommentPage
 * @param next_page
 * @param flag
 * @desc 切换项目数据页面
 *      1. 判断按钮性质，计算目标页码
 *      2. 判断目标页码合理性，换页
 */
function changeCommentPage(next_page, flag)
{
    var page = document.querySelector('#post-detail > div:nth-child(7) > div.row > div > div');

    if (flag) {
        next_page = next_page + now_comment_page;
    }

    if (next_page >= 1 && next_page <= comment_page_cnt) {
        now_comment_page = next_page;
        writeComment(now_comment_page);
        if (comment_page_cnt > 9) {
            if (now_comment_page + 4 > comment_page_cnt) {
                createPage(page, comment_page_cnt - 8, comment_page_cnt, 'changeCommentPage', now_comment_page);
            } else if (now_comment_page - 4 < 1) {
                createPage(page,1, 9, 'changeCommentPage', now_comment_page);
            } else {
                createPage(page,now_comment_page - 4, now_comment_page + 4, 'changeCommentPage', now_comment_page);
            }
        } else {
            createPage(page,1, comment_page_cnt, 'changeCommentPage', now_comment_page);
        }
    }
}

/**
 * @method main
 * @desc 增加几个按钮的切换效果，创建post
 */
function main()
{
    document.querySelector('#post-detail > div.row.control-bar > div.col-md-2 > a').onclick = function(){
        document.querySelector('#post-list').classList.remove('hidden');
        document.querySelector('#post-list').classList.add('show');
        document.querySelector('#post-detail').classList.remove('show');
        document.querySelector('#post-detail').classList.add('hidden');
    };
    document.querySelector('#add-post-btn > div.col-md-2 > a').onclick = function(){
        document.querySelector('#post-list').classList.remove('show');
        document.querySelector('#post-list').classList.add('hidden');
        document.querySelector('#add-post').classList.remove('hidden');
        document.querySelector('#add-post').classList.add('show');
    };
    document.querySelector('#add-post-btn > div:nth-child(3) > a').onclick = function() {
        document.querySelector('#post-list').classList.remove('hidden');
        document.querySelector('#post-list').classList.add('show');
        document.querySelector('#add-post').classList.remove('show');
        document.querySelector('#add-post').classList.add('hidden');
    };
    createPost();
}

main();