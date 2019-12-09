function ShowElement(element) {
    var newobj = document.createElement('textarea');

    var oldContent = element.innerHTML;
    var key = element.getAttribute('id');

    newobj.type = 'text';
    newobj.value = oldContent;
    newobj.style.height = key == 'introduction' ? '9rem' : '2rem';
    newobj.style.width = '100%';
    newobj.onblur = function () {
        element.innerHTML = this.value;
        element.setAttribute("ondblclick", "ShowElement(this);");
        if (key != 'model' && element.innerHTML.length <= 0) {
            alert('Can not be empty!');
            element.innerHTML = oldContent;
            return;
        }
        if (key == 'model' && element.innerHTML.length > 200) {
            alert("Length of content can not surpass 200!");
            element.innerHTML = oldContent;
            return;
        }
        if (key != 'model' && element.innerHTML.length > 2000) {
            alert("Length of content can not surpass 2000!");
            element.innerHTML = oldContent;
            return;
        }
        $.ajax({
            'url': '/project/update/',
            'type': 'post',
            'data': {
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
                'key': key,
                'text': this.value,
                'pid': pid
            },
            success: function (msg) {
                if (msg == 'Fail') {
                    alert("Please fill in the blank with valid content!");
                    element.innerHTML = oldContent;
                }
            }
        });
    };
    element.innerHTML = '';
    element.appendChild(newobj);
    newobj.setSelectionRange(0, oldContent.length);
    newobj.focus();
    newobj.parentElement.setAttribute("ondblclick", "")
}

function del() {
    var msg = "您真的要删除项目吗？";
    if (confirm(msg)) {
        $.ajax({
            'url': '/project/delete/',
            'type': 'post',
            async: false,
            'data': {
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
                'pid': pid
            },
            success: function (data) {
                new_url = "http://" + window.location.host + "/project/domain/" + data + "/";
                window.location.href = new_url;
            },
            error: function (msg) {
                alert(msg)
            }
        });
    } else {
        return false;
    }
}

function project_echarts() {
    var dom = document.getElementById("container");
    var myChart = echarts.init(dom);
    option = null;

    t.sort(function (a, b) {
        return a - b;
    });
    var dataAxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'];
    dataAxis.reverse();
    var yMax = t[t.length - 1];
    var dataShadow = [];

    for (var i = 0; i < data.length; i++) {
        dataShadow.push(yMax);
    }
    option = {
        xAxis: {
            data: dataAxis,
            axisLabel: {
                inside: false,
                textStyle: {
                    color: '#000000'
                }
            },
            axisTick: {
                show: false
            },
            axisLine: {
                show: false
            },
            z: 10
        },
        yAxis: {
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                textStyle: {
                    color: '#999'
                }
            }
        },
        dataZoom: [
            {
                type: 'inside'
            }
        ],
        series: [
            { // For shadow
                type: 'bar',
                itemStyle: {
                    normal: {color: 'rgba(0,0,0,0.05)'}
                },
                barGap: '-100%',
                barCategoryGap: '40%',
                data: dataShadow,
                animation: false
            },
            {
                type: 'bar',
                itemStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(
                            0, 0, 0, 1,
                            [
                                {offset: 0, color: '#fdffaf'},
                                {offset: 0.5, color: '#f0d473'},
                                {offset: 1, color: '#f0d473'}
                            ]
                        )
                    },
                    emphasis: {
                        color: new echarts.graphic.LinearGradient(
                            0, 0, 0, 1,
                            [
                                {offset: 0, color: '#f0d473'},
                                {offset: 0.7, color: '#f0d473'},
                                {offset: 1, color: '#fffbe6'}
                            ]
                        )
                    }
                },
                data: data
            }
        ]
    };

    // Enable data zoom when user click bar.
    var zoomSize = 6;
    myChart.on('click', function (params) {
        console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
        myChart.dispatchAction({
            type: 'dataZoom',
            startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
            endValue: dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
        });
    });
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}

function paint(mydata, max, id) {
    var optionMap = {
        // backgroundColor: '#FFFFFF',
        tooltip: {
            trigger: 'item'
        },

        //左侧小导航图标
        visualMap: {
            show: true,
            x: 'left',
            y: 'center',
            min: 0,
            max: max,
            // color: ['#ffffdf','#ffffbf', '#fef0af','#fed090', '#febe81', '#fdae61', '#f46d43', '#e46d43', '#d73027',  '#c73027', '#a50026'].reverse()
            inRange: {
                color: ['#FFFFCC', '#E15457']
            }
        },
        //配置属性
        series: [{
            name: '数据',
            type: 'map',
            mapType: 'china',
            roam: true,
            label: {
                normal: {
                    show: false  //省份名称
                },
                emphasis: {
                    show: false
                }
            },
            data: mydata  //数据
        }]
    };
    //初始化echarts实例
    var myChart = echarts.init(document.getElementById(id));
    //使用制定的配置项和数据显示图表
    myChart.setOption(optionMap);
}

function initpaint() {
    paint(mydata_week, max_week, 'container-1');
    paint(mydata_month, max_month, 'container-2');
    paint(mydata_year, max_year, 'container-3');
    document.querySelector("#c-5").style.display = "none";
    document.querySelector("#c-6").style.display = "none";
}

function showMap(id) {
    document.querySelector("#c-4").style.display = "none";
    document.querySelector("#c-5").style.display = "none";
    document.querySelector("#c-6").style.display = "none";
    document.querySelector(id).style.display = "";
}