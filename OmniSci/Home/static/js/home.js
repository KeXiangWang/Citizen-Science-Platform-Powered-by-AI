
/**
 * @method writePopularProject
 * @param page_num int 填充页数
 * @desc 填充项目缩略图，项目日期，项目具体内容
 */
function writePopularProject(page_num)
{
    var i, len = popular_project.length;
    var num = len > 0 ? (page_num == Math.ceil(len / 3) ? (len - 1) % 3 + 1 : 3) : 0;

    for (i = 3;i >= 1;i --) {
        var container = document.querySelector('#popular-project-container > div > div:nth-child(1) > ' +
            'div:nth-child(' + i + ')');

        if (i <= num) {
            container.style.display = 'block';

            var content = popular_project[(page_num - 1) * 3 + i - 1];

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

            project_name.href = '/project/detail/' + content['pid'] + '/';
            header.children[0].href = '/project/detail/' + content['pid'] + '/';
            link.href = '/project/detail/' + content['pid'] + '/';
            join.href = '/project/detail/' + content['pid'] + '/';
        } else {
            container.style.display = 'none';
        }
    }
}

/**
 * @method writeCategoryProject
 * @param category int 填充分类编号
 * @param page_num int 填充页数
 * @desc 填充项目缩略图，项目名称，项目发起人
 */
function writeCategoryProject(category, page_num)
{
    var i, len = category_project[category].length;
    var num = len > 0 ? (page_num == Math.ceil(len / 6) ? (len - 1) % 6 + 1 : 6) : 0;

    for (i = 6;i >= 1;i --) {
        var container = document.querySelector('#category-container > div > div:nth-child(1) > ' +
            'div:nth-child(' + Math.ceil(i / 3) + ') > div:nth-child(' + ((i - 1) % 3 + 1) + ')');

        if (i <= num) {
            container.style.display = 'block';
            var content = category_project[category][(page_num - 1) * 6 + i - 1];

            var image = container.children[0].children[0].children[0];
            var name = container.children[0].children[1].children[0].children[0];
            var owner = container.children[0].children[1].children[1];

            image.children[0].src = content['projection_image'];

            name.innerHTML = content['projection_name'];

            owner.innerHTML = "<i class=\"fa fa-user\"></i>发起人 <span>Owner：</span> " +
                content['user_name'];

            name.href = '/project/detail/' + content['pid'] + '/';
            image.href = '/project/detail/' + content['pid'] + '/';
        } else {
            container.style.display = 'none';
        }
    }
}

/**
 * @method createPopularPage
 * @desc 创建热门项目框架
 *      1. 根据项目数更换换页按钮
 *      2. 显示第一页
 */
function createPopularPage()
{
    var i, page_cnt = Math.ceil(popular_project.length / 3);

    var page = document.querySelector('#popular-project-container > div > div:nth-child(2) > div');
    if (page_cnt <= 1) {
        page.parentNode.removeChild(page);
    } else {
        createPage(page.children[0], 1, page_cnt, "changePopularPage", 1);
    }

    // 填充第一页
    writePopularProject(1);
}

/**
 * @method createCategory
 * @desc 创建项目分类标签
 */
function createCategory()
{
    var i = 1, container = document.querySelector('#domain_label');
    for (var key in category_project) {
        var factor = document.createElement('span');
        factor.innerHTML = '<i class="fa fa-paper-plane-o icon"></i><a href="javascript:void(0)">' + key +'</a>';
        container.appendChild(factor);
        $('#domain_label > span:nth-child(' + i + ')').attr('onclick', 'changeCategory(' + i + ')');
        i ++;
    }

    if (i > 1) {
        document.querySelector('#domain_label > span:nth-child(1)').classList.add('category-active');
    }

    if (category_num.length == 0) {
        category_num.push(0);
        category.push('null');
        category_project['null'] = [];
    }

    createPage(document.querySelector('#category-container > div > div:nth-child(2) > div > div'),
        1, Math.ceil(category_num[0] / 6), 'changeCategoryPage', 1);
    writeCategoryProject(category[0], 1);
}

var popular_now_page = 1;
/**
 * @method changePopularPage
 * @param next_page int 目标页面 / 上一页或者下一页
 * @param flag bool 换页标志 false: next_page 表示目标页 true: next_page 表示上下页 (1 - 下一页 -1 - 上一页)
 * @desc 切换热门项目页面
 *      1. 判断按钮性质，计算目标页码
 *      2. 判断目标页码合理性，换页
 */
function changePopularPage(next_page, flag)
{
    var page_num = Math.ceil(popular_project.length / 3);
    if (flag) {
        next_page = next_page + popular_now_page;
    }
    if (next_page >= 1 && next_page <= page_num) {

        document.querySelector('#popular-project-container > div > div:nth-child(2) > div > div > ul > ' +
            'li:nth-child(' + (popular_now_page + 1) + ') > a').classList.remove('choosed-page');
        document.querySelector('#popular-project-container > div > div:nth-child(2) > div > div > ul > ' +
            'li:nth-child(' + (next_page + 1) + ') > a').classList.add('choosed-page');
        writePopularProject(next_page);
        popular_now_page = next_page;
    }
}

var now_category = 1;
var now_page = 1;
/**
 * @method changeCategory
 * @param next_category int 目标类别编号
 * @desc 切换分类项目类别
 *      1. 判断当前项目与目标项目是否相同
 *      2. 重新生成页框
 *      3. 写入数据
 */
function changeCategory(next_category)
{
    if (next_category != now_category) {
        createPage(document.querySelector('#category-container > div > div:nth-child(2) > div > div'),
        1, Math.ceil(category_num[next_category - 1] / 6), 'changeCategoryPage', 1);
        writeCategoryProject(category[next_category - 1], 1);
        document.querySelector('#domain_label > span:nth-child(' + now_category +')').classList.remove('category-active');
        document.querySelector('#domain_label > span:nth-child(' + next_category +')').classList.add('category-active');
        now_category = next_category;
        now_page = 1;
    }
}

/**
 * @method changeCategoryPage
 * @param next_page int 目标页面 / 上一页或者下一页
 * @param flag bool 换页标志 false: next_page 表示目标页 true: next_page 表示上下页 (1 - 下一页 -1 - 上一页)
 * @desc 切换热门项目页面
 *      1. 判断按钮性质，计算目标页码
 *      2. 判断目标页码合理性，换页
 */
function changeCategoryPage(next_page, flag)
{
    var page_num = Math.ceil(category_num[now_category - 1] / 6);
    if (flag) {
        next_page = next_page + now_page;
    }
    if (next_page >= 1 && next_page <= page_num) {

        document.querySelector('#category-container > div > div:nth-child(2) > div > div > ul > ' +
            'li:nth-child(' + (now_page + 1) +') > a').classList.remove('choosed-page');
        document.querySelector('#category-container > div > div:nth-child(2) > div > div > ul > ' +
            'li:nth-child(' + (next_page + 1) +') > a').classList.add('choosed-page');
        writeCategoryProject(category[now_category - 1], next_page);
        now_page = next_page;
    }
}

var category_num = [];
var category = [];
/**
 * @method main
 * @desc 主函数
 *      1. 创建热门项目与分类项目框架
 *      2. 填充项目具体内容
 */
function main()
{
    for (var key in category_project) {
        category_num.push(category_project[key].length);
        category.push(key);
    }
    createPopularPage();
    createCategory();
}

main();