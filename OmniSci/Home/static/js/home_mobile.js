$(function() {

    var mescroll = new initMeScroll("mescroll", {
        down: {
            auto: false,
            callback: downCallback,
        },
        up: {
            auto: false,
            isBoth: true,
            page: {
				num: 0,
				size: 10,
			},
            callback: upCallback,
        }
    });

    function downCallback() {
        $.ajax({
            type: "POST",
            datatype: "json",
            data: {
                'page_cnt': 0
            },
            url: "/home/index/",
            success: function (data) {
                mescroll.endSuccess();
                var container = document.querySelector("#project");
                container.innerHTML = '';
                for (var i = 0; i < data.popular.length; i ++) {
                    var element = document.createElement('div');
                    var project = data.popular[i];
                    element.className = 'card col-xs-10 col-sm-6 col-lg-4 mb-3 p-0';
                    element.innerHTML =
                        '<a href="/project/detail/' + project['pid'] + '/">\n' +
                        '    <img class="card-img-top" src="' + project['projection_image'] + '" style="height: 10rem">\n' +
                        '</a>\n' +
                        '<div class="card-body">\n' +
                        '    <div class="row justify-content-between">\n' +
                        '        <div class="col-8">\n' +
                        '            <a href="/project/detail/' + project['pid'] + '/">\n' +
                        '                <h6 class="card-title text-truncate text-theme">' + project['projection_name'] + '</h6>\n' +
                        '            </a>\n' +
                        '        </div>\n' +
                        '        <div class="col-4">\n' +
                        '            <h6 class="text-truncate text-theme"><small>' + project['user_name'] + '</small></h6>\n' +
                        '        </div>\n' +
                        '    </div>\n' +
                        '    <p class="card-text text-truncate"><small>' + project['projection_introduction'] + '</small></p>\n' +
                        '    <div class="row justify-content-center">\n' +
                        '        <a href="/project/detail/' + project['pid'] + '/" class="btn btn-outline-theme text-center">查看更多 More</a>\n' +
                        '    </div>\n' +
                        '</div>';
                    container.appendChild(element);
                }
            },
            error : function() {
                mescroll.endErr();
            }
        });
    }

    function upCallback(page) {
        $.ajax({
            type: "POST",
            datatype: "json",
            data: {
                'page_cnt': page.num
            },
            url: "/home/index/",
            success: function (data) {
                var hasNext = data.total_project > ((page.num + 1) * 10 + data.popular.length);
                mescroll.endSuccess(data.popular.length, hasNext);
                var container = document.querySelector("#project");
                for (var i = 0; i < data.popular.length; i ++) {
                    var element = document.createElement('div');
                    var project = data.popular[i];
                    element.className = 'card col-xs-10 col-sm-6 col-lg-4 mb-3 p-0';
                    element.innerHTML =
                        '<a href="/project/detail/' + project['pid'] + '/">\n' +
                        '    <img class="card-img-top" src="' + project['projection_image'] + '" style="height: 10rem">\n' +
                        '</a>\n' +
                        '<div class="card-body">\n' +
                        '    <div class="row justify-content-between">\n' +
                        '        <div class="col-8">\n' +
                        '            <a href="/project/detail/' + project['pid'] + '/">\n' +
                        '                <h6 class="card-title text-truncate text-theme">' + project['projection_name'] + '</h6>\n' +
                        '            </a>\n' +
                        '        </div>\n' +
                        '        <div class="col-4">\n' +
                        '            <h6 class="text-truncate text-theme"><small>' + project['user_name'] + '</small></h6>\n' +
                        '        </div>\n' +
                        '    </div>\n' +
                        '    <p class="card-text text-truncate"><small>' + project['projection_introduction'] + '</small></p>\n' +
                        '    <div class="row justify-content-center">\n' +
                        '        <a href="/project/detail/' + project['pid'] + '/" class="btn btn-outline-theme text-center">查看更多 More</a>\n' +
                        '    </div>\n' +
                        '</div>';
                    container.appendChild(element);
                }
            },
            error : function() {
                mescroll.endErr();
            }
        });
    }

    document.ondragstart=function() {return false;}
});