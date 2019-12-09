
function setSideBar()
{
    var box = document.getElementById("side-bar");
    var btn = document.getElementById("side-bar-btn");
    var overlay = document.getElementById('page-overlay');
    btn.onclick = function() {
        if (box.offsetLeft == 0) {
            box.style['margin-left'] = '-60%';
            overlay.style['display'] = 'none';
        } else {
            box.style['margin-left'] = '0';
            overlay.style['display'] = 'block';
        }
    };

    overlay.onclick = function () {
        box.style['margin-left'] = '-60%';
        overlay.style['display'] = 'none';
    };
}

function moveEvent()
{
    var body = $("body");
    body.css("height", $(window).height());

    body.on("touchstart", function(e) {
        startX = e.originalEvent.changedTouches[0].pageX;
        startY = e.originalEvent.changedTouches[0].pageY;
　　});

　　body.on("touchmove", function(e) {
        var moveEndX = e.originalEvent.changedTouches[0].pageX;
        var moveEndY = e.originalEvent.changedTouches[0].pageY;

        var x = moveEndX - startX;
        var y = moveEndY - startY;

        var box = document.getElementById("side-bar");
        var overlay = document.getElementById('page-overlay');

        if (Math.abs(x) > Math.abs(y) && x > 30 ) {
            box.style['margin-left'] = '0';
            overlay.style['display'] = 'block';
        }
        else if (Math.abs(x) > Math.abs(y) && x < -30 ) {
            box.style['margin-left'] = '-60%';
            overlay.style['display'] = 'none';
        }
        else if (Math.abs(x) <= Math.abs(y) && y > 0 ) {

        }
        else if (Math.abs(x) <= Math.abs(y) && y < 0 ) {

        }
    });
}

setSideBar();
moveEvent();