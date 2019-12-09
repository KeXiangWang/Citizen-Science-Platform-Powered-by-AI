/**
 * @desc 获取热门项目和热门领域数据，并渲染
 */
$.ajax({
    type: "POST",
    dataType: "json",
    url: "/project/search/",
    data: {"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
    success: function (data) {
        domain = data.domain;
        projects = data.projects;
        writePopularProject(document.querySelector('body > div.page-wrapper > section > div > div >' +
            ' div.col-md-4 > div > div > div:nth-child(3)'), projects);
        createCategory(document.querySelector('body > div.page-wrapper > section > div > div >' +
            ' div.col-md-4 > div > div > div:nth-child(2) > div'), domain);
    },
    error : function() {}
});