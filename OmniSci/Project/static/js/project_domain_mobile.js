
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
				size: 20,
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
            url: "/project/domain/" + domain_name + '/',
            success: function (data) {
                mescroll.endSuccess();
                var container = document.querySelector("#project");
                container.innerHTML = '';
                for (var i = 0; i < data.domain_project.length; i ++) {
                    var element = document.createElement('div');
                    var project = data.domain_project[i];
                    element.className = 'col-11 col-md-5 mt-2 mx-0 p-0 rounded';
                    element.innerHTML =
                    '<div class="row m-0 p-0" style="box-shadow: 1px 1px 3px #333333">\n' +
                    '    <a href="/project/detail/' + project['pid'] + '/" class="col-4 mr-0 rounded p-0">\n' +
                    '        <img src="' + project['projection_image'] + '" style="height: 7rem; width: 100%;">\n' +
                    '    </a>' +
                    '    <div class="col-8 mr-0">\n' +
                    '        <a href="/project/detail/' + project['pid'] + '/">\n' +
                    '            <h5 class="text-theme text-truncate"><small>' + project['projection_name'] + '</small></h5>\n' +
                    '        </a>' +
                    '        <h6 class="text-theme text-truncate"><small><span class="badge badge-theme mr-1">发起人</span>' + project['user_name'] + '</small></h6>\n' +
                    '        <p class="text-truncate-2 m-0">\n' +
                    '            ' + project['projection_introduction'] +'\n' +
                    '        </p>\n' +
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
            url: "/project/domain/" + domain_name + '/',
            success: function (data) {
                var hasNext = data.total_project > ((page.num + 1) * 10 + data.domain_project.length);
                mescroll.endSuccess(data.domain_project.length, hasNext);

                var container = document.querySelector("#project");
                for (var i = 0; i < data.domain_project.length; i ++) {
                    var element = document.createElement('div');
                    var project = data.domain_project[i];
                    element.className = 'col-11 col-md-5 mt-2 mx-0 p-0 rounded';
                    element.innerHTML =
                    '<div class="row m-0 p-0" style="box-shadow: 1px 1px 3px #333333">\n' +
                    '    <a href="/project/detail/' + project['pid'] + '/" class="col-4 mr-0 rounded p-0">\n' +
                    '        <img src="' + project['projection_image'] + '" style="height: 7rem; width: 100%;">\n' +
                    '    </a>' +
                    '    <div class="col-8 mr-0">\n' +
                    '        <a href="/project/detail/' + project['pid'] + '/">\n' +
                    '            <h5 class="text-theme text-truncate"><small>' + project['projection_name'] + '</small></h5>\n' +
                    '        </a>' +
                    '        <h6 class="text-theme text-truncate"><small><span class="badge badge-theme mr-1">发起人</span>' + project['user_name'] + '</small></h6>\n' +
                    '        <p class="text-truncate-2 m-0">\n' +
                    '            ' + project['projection_introduction'] +'\n' +
                    '        </p>\n' +
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