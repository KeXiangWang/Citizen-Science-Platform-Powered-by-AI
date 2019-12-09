
/**
 * @method writeProject
 * @param container dom 热门项目容器
 * @param projects array 热门项目
 * @desc 填充热门项目图片，项目名称，项目日期
 *      1. 填充数据
 *      2. 删除多余元素
 */
function writePopularProject(container, projects)
{
    for (var i = 1;i <= projects.length;i ++) {

        container.children[i].style.display = 'block';

        var image = container.children[i].children[0].children[0];

        var name = container.children[i].children[1].children[0].children[0];

        var date_container = container.children[i].children[1].children[1];

        image.children[0].src = projects[i - 1]['projection_image'];

        name.innerHTML = projects[i - 1]['projection_name'];

        image.href = '/project/detail/' + projects[i - 1]['pid'] + '/';
        name.href = '/project/detail/' + projects[i - 1]['pid'] + '/';

        date_container.innerHTML = '<i class="fa fa-clock-o"></i>' + projects[i - 1]['publish_time'];
    }

    for (i = projects.length + 1;i <= 6;i ++) {
        var rest = container.children[projects.length + 1];
        rest.parentNode.removeChild(rest);
    }
}

/**
 * @method createCategory
 * @param container dom 热门领域容器
 * @param domain array 热门领域
 * @desc 创建项目分类标签
 */
function createCategory(container, domain)
{
    for (var i = 0;i < domain.length;i ++) {
        var factor = document.createElement('span');
        factor.innerHTML = '<i class="fa fa-paper-plane-o icon"></i><a href="/project/domain/'
            + domain[i]['domain_name'] + '">' + domain[i]['domain_name'] + '</a>';
        container.appendChild(factor);
    }
}

/**
 * @method createPage
 * @param page_container dom 页码容器
 * @param mn int 页码最小值
 * @param mx int 页码最大值
 * @param change str 换页函数
 * @param now int 当前页码
 * @desc 创建一定数量的页码框
 */
function createPage(page_container, mn, mx, change, now)
{
    var container = page_container.children[0];
    container.innerHTML = "";

    if (mx - mn <= 0)
        return;

    var i, page = document.createElement('li');
    page.innerHTML = '<a href="javascript:void(0)"><i class="fa fa-angle-left" style="color: black"></i></a>';
    container.appendChild(page);

    for (i = mn;i <= mx;i ++) {
        page = document.createElement('li');
        page.innerHTML = '<a href="javascript:void(0)">' + i + '</a>';
        container.appendChild(page);
    }

    page = document.createElement('li');
    page.innerHTML = '<a href="javascript:void(0)"><i class="fa fa-angle-right" style="color: black"></i></a>';
    container.appendChild(page);

    $(container.children[0]).attr('onclick', change + '(-1, true);');

    for (i = mn;i <= mx;i ++) {
        $(container.children[i - mn + 1]).attr('onclick', change + '(' + i + ', false);');
    }

    $(container.children[mx - mn + 2]).attr('onclick', change + '(1, true);');

    container.children[now - mn + 1].children[0].classList.add('choosed-page');
}