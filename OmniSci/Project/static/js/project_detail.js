var now_board = 1;
var verified = 1;
var audition = true;

var board_map = {'image': 1, 'forum': 2, 'submit': 3, 'unaudited': 4,'audited': 5, 'manage': 6};
var button_board_map = [0, 2, 3, 4, 2, 2, 5];

/**
 * @method changeBoard
 * @param next_board 目标板块
 * @desc 判断目标板块与当前板块是否相同，然后切换
 */
function changeBoard(next_board) {
    if (now_board == next_board) {
        return;
    }

    // 修改按钮样式
    document.querySelector('#info-content-divider > div.row.sidebar-left >' +
        ' span:nth-child(' + now_board + ') > a').classList.remove('choosed-btn-3');
    document.querySelector('#info-content-divider > div.row.sidebar-left >' +
        ' span:nth-child(' + next_board + ') > a').classList.add('choosed-btn-3');

    // 修改板块显示
    document.querySelector('#info-content-divider >' +
        ' div:nth-child(' + button_board_map[now_board] + ')').classList.add('inactive-project-section');
    document.querySelector('#info-content-divider >' +
        ' div:nth-child(' + button_board_map[next_board] + ')').classList.remove('inactive-project-section');

    now_board = next_board;

    if (now_board == board_map['manage']) {
        project_echarts();
        initpaint()
    }

    if (authority  < 3 && (now_board == board_map['image'] || now_board == board_map['unaudited'] || now_board == board_map['audited'])) {
        document.querySelector('#info-content-divider > div:nth-child(2)').style.visibility = 'hidden';
        var i;
        switch (now_board) {
            // 成果库
            case board_map['image']:
                document.querySelector('#audited').style.display = 'none';
                document.querySelector('#audition-all').style.display = 'none';
                document.querySelector('#audited-accept-all').style.display = 'none';
                document.querySelector('#audited-decline-all').style.display = 'none';
                for (i = 1; i <= 9; i++) {
                    document.querySelector('#audition_' + i).style.display = 'none';
                    document.querySelector('#accepted_' + i).style.display = 'none';
                    document.querySelector('#declined_' + i).style.display = 'none';
                }
                verified = 1;
                break;
            // 审核区
            case board_map['unaudited']:
                document.querySelector('#audited').style.display = 'none';
                document.querySelector('#audition-all').style.display = 'block';
                document.querySelector('#audited-accept-all').style.display = 'none';
                document.querySelector('#audited-decline-all').style.display = 'none';
                for (i = 1; i <= 9; i++) {
                    document.querySelector('#audition_' + i).style.display = 'block';
                    document.querySelector('#accepted_' + i).style.display = 'none';
                    document.querySelector('#declined_' + i).style.display = 'none';
                }
                verified = 0;
                break;
            // 已审核区
            case board_map['audited']:
                document.querySelector('#audited').style.display = 'block';
                document.querySelector('#audition-all').style.display = 'none';
                document.querySelector('#audited-accept-all').style.display = 'block';
                document.querySelector('#audited-decline-all').style.display = 'none';
                for (i = 1; i <= 9; i++) {
                    document.querySelector('#audition_' + i).style.display = 'none';
                    document.querySelector('#accepted_' + i).style.display = 'block';
                    document.querySelector('#declined_' + i).style.display = 'none';
                }
                audition = true;
                verified = 1;
                document.querySelector('#audited > div:nth-child(1) > a').classList.add('choosed-btn');
                document.querySelector('#audited > div:nth-child(2) > a').classList.remove('choosed-btn');

                break;
        }
        $.ajax({
            type: "POST",
            datatype: "json",
            data: {
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            url: "/project/detail_page_cnt/" + pid + "/" + verified + "/",
            success: function (data) {
                page_cnt = data.page_cnt;
                createData();
                document.querySelector('#info-content-divider > div:nth-child(2)').style.visibility = 'visible';
            },
            error: function (msg) {
                alert(msg);
            }
        });
    }
}

/**
 * @method writeProject
 * @param page_num 页数
 * @desc 填充数据图片，数据上传者，数据上传日期
 */
function writeData(page_num) {
    $.ajax({
        type: "POST",
        datatype: "json",
        data: {"csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()},
        url: "/project/detail_page/" + pid + "/" + page_num + "/" + verified + "/",
        success: function (data) {
            var project_data = data.data;
            var i, num = project_data.length;

            for (i = 9; i >= 1; i--) {
                var container = document.querySelector('#data_' + i);

                var image = container.children[0];
                var img = container.children[1];
                var publisher = container.children[2].children[0].children[0];
                var data_type = container.children[2].children[0].children[1];

                if (i <= num) {
                    container.style.display = 'block';

                    if (authority  < 3 && now_board == board_map['unaudited']) {
                        document.querySelector('#audition_' + i).style.display = 'block';
                    }

                    if (authority  < 3 && now_board == board_map['audited'] && audition) {
                        document.querySelector('#accepted_' + i).style.display = 'block';
                    }

                    if (authority  < 3 && now_board == board_map['audited'] && !audition) {
                        document.querySelector('#declined_' + i).style.display = 'block';
                    }

                    var content = project_data[i - 1];

                    image.src = content['data_path'];

                    img.href = content['data_path'];

                    publisher.innerHTML = '<i class="fa fa-user icon"></i><span>' + content['user_name'] + '</span>';

                    data_type.innerHTML = '<i class="fa fa-binoculars icon" ></i>' + content['data_name'];
                } else {
                    container.style.display = 'none';

                    if (authority  < 3 && now_board == board_map['unaudited']) {
                        document.querySelector('#audition_' + i).style.display = 'none';
                    }

                    if (authority  < 3 && now_board == board_map['audited'] && audition) {
                        document.querySelector('#accepted_' + i).style.display = 'none';
                    }

                    if (authority  < 3 && now_board == board_map['audited'] && !audition) {
                        document.querySelector('#declined_' + i).style.display = 'none';
                    }

                    image.src = '/static/project_data/white.png';

                    img.href = '/static/project_data/white.png';
                }

                if (authority  < 3) {
                    var audition_area = document.querySelector('#audition_' + i);
                    var decline_area = document.querySelector('#declined_' + i);
                    var accept_area = document.querySelector('#accepted_' + i);


                    $(audition_area.children[0]).removeAttr('onclick');
                    $(audition_area.children[1]).removeAttr('onclick');
                    $(decline_area.children[0]).removeAttr('onclick');
                    $(decline_area.children[1]).removeAttr('onclick');
                    $(accept_area.children[0]).removeAttr('onclick');

                    if (i <= num) {
                        if (now_board == board_map['unaudited']) {
                            $(audition_area.children[0]).attr('onclick',
                                'userAudition(' + content['data_id'] + ', "accept")');
                            $(audition_area.children[1]).attr('onclick',
                                'userAudition(' + content['data_id'] + ', "decline")');
                        }

                        if (now_board == board_map['audited'] && audition) {
                            $(accept_area.children[0]).attr('onclick',
                                'userAudition(' + content['data_id'] + ', "decline")');
                        }

                        if (now_board == board_map['audited'] && !audition) {
                            $(decline_area.children[0]).attr('onclick',
                                'userAudition(' + content['data_id'] + ', "accept")');
                            $(decline_area.children[1]).attr('onclick',
                                'userAudition(' + content['data_id'] + ', "delete")');
                        }
                    }
                }
            }
        },
        error: function (msg) {
            alert(msg);
        }
    });
}

var now_page = 1;

/**
 * @method createData
 * @desc 完成数据填充
 *      1. 创建换页框
 *      2. 填充数据
 */
function createData() {
    var i;
    var page = document.querySelector('#project-data-page > div');

    // 处理换页框
    if (page_cnt <= 1) {
        page.style.display = 'none';
    } else {
        page.style.display = 'block';
        createPage(page.children[0], 1, Math.min(page_cnt, 9), 'changePage', 1);
    }

    now_page = 1;
    // 写入第一页数据
    writeData(1);
}

/**
 * @method changePage
 * @param next_page
 * @param flag
 * @desc 切换项目数据页面
 *      1. 判断按钮性质，计算目标页码
 *      2. 判断目标页码合理性，换页
 */
function changePage(next_page, flag) {
    var page = document.querySelector('#project-data-page > div > div');

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

/**
 * @method
 * @desc 即时显示用户上传的项目图片
 *      1. 获取图片位置，转化为可显示url
 *      2. 判断图片格式，返回错误
 *      3. 显示图片
 */
$('#user-submit').on('change', function () {
    var filePath = $(this).val();
    var fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase();
    var src = window.URL.createObjectURL(this.files[0]);

    if (!fileFormat.match(/.png|.jpg|.jpeg|.PNG|.JPG|.JPEG/)) {
        return;
    }

    $('#user-upload-img').attr('src', src);
});

createData();