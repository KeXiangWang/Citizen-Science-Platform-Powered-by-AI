/*
* 用户信息界面修改个人信息栏的js代码
*
* */



//修改密码

$('#change-pwd')[0].onclick = () => {
    // console.log("clicked");
    layer.open({
        area: [window.innerWidth + 'px', window.innerHeight + 'px'],
        title: "修改密码",
        type: 2,                             //0:信息框;1:页面层;2:iframe层;3:加载层;4:tips层
        content: "/user/change-pwd/",
    });
}

$('#delete-account')[0].onclick = () => {
    const os = getOs();
    let br = '\r\n';
    let content = 'Fail';
    if (os == 'FF' || os == 'SF') {
        br = '\n';
    }
    const msg = "删除账户意味着丢失所有的数据，是否继续当前操作?" + br +
        "Deleting the account means losing all your data, are you sure to continue the operation?";
    //危险操作，确认一下
    const res = confirm(msg);

    if (res) {
        layer.open({
            area: [window.innerWidth*3/4 + 'px', window.innerHeight*2/3 + 'px'],
            title: "删除账户",
            type: 2,                             //0:信息框;1:页面层;2:iframe层;3:加载层;4:tips层
            content: "/user/delete-account/",
        });
    }
}

$('#change-info')[0].onclick = () => {
    layer.open({
        area: [window.innerWidth + 'px', window.innerHeight + 'px'],
        title: "修改个人信息",
        type: 2,                             //0:信息框;1:页面层;2:iframe层;3:加载层;4:tips层
        content: "/user/change-info/",
    });
}