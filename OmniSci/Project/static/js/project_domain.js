/**
 * @method writeProject
 * @param page_num 页数
 * @desc 填充数据图片，数据上传者，数据上传日期
 */
function writeData(page_num)
{
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {
            "csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val(),
            "page_cnt": page_num - 1
        },
        url: "/project/domain/" + domain_name + "/",
        success: function (data) {
            var domain_projects = data.domain_project;
            var i, num = domain_projects.length;

            for (i = 6;i >= 1;i --) {
                var container = document.querySelector('#domain_' + i);

                if (i <= num) {
                    container.style.display = 'block';

                    var content = domain_projects[i - 1];

                    var header = container.children[0].children[0];
                    var date = content['publish_time'].split('-');

                    var month=["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"];

                    header.children[0].children[0].src = content['projection_image'];
                    header.children[1].children[0].innerHTML = date[2] + 'th <span>' +
                        month[parseInt(date[1]) - 1] + " > " + date[0] + "</span>";

                    var detail = container.children[0].children[1];
                    var project_name = detail.children[0].children[0];
                    var project_end_time = detail.children[1].children[0].children[1];
                    var link = detail.children[2];
                    var join = detail.children[3];

                    project_name.children[0].innerHTML = content['projection_name'];
                    project_end_time.innerHTML = (parseInt(date[0]) + 2) + '/' + date[1] + '/' + date[2];

                    header.children[0].href = '/project/detail/' + content['pid'] + '/';
                    project_name.href = '/project/detail/' + content['pid'] + '/';
                    link.href = '/project/detail/' + content['pid'] + '/';
                    join.href = '/project/detail/' + content['pid'] + '/';
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
 * @method createData
 * @desc 完成数据填充
 *      1. 创建换页框
 *      2. 创建一定数量数据容器
 *      3. 填充数据
 */
function createData()
{
    var page = document.querySelector('#domain_page');

    // 处理换页框
    if (page_cnt <= 1) {
        page.parentNode.removeChild(page);
    } else {
        createPage(page.children[0], 1, Math.min(page_cnt, 9), 'changePage', 1);
    }

    // 写入第一页数据
    writeData(1);
}

var now_page = 1;
/**
 * @method changePage
 * @param next_page
 * @param flag
 * @desc 切换项目数据页面
 *      1. 判断按钮性质，计算目标页码
 *      2. 判断目标页码合理性，换页
 */
function changePage(next_page, flag)
{
    var page = document.querySelector('#domain_page > div');

    if (flag) {
        next_page = next_page + now_page;
    }

    if (next_page >= 1 && next_page <= page_cnt) {
        now_page = next_page;
        writeData(now_page);
        if (page_cnt > 9) {
            if (now_page + 4 > page_cnt) {
                createPage(page, page_cnt - 8, page_cnt, 'changePage', now_page);
            } else if (now_page - 4 < 1) {
                createPage(page, 1, 9, 'changePage', now_page);
            } else {
                createPage(page, now_page - 4, now_page + 4, 'changePage', now_page);
            }
        } else {
            createPage(page, 1, page_cnt, 'changePage', now_page);
        }
    }
}

createData();