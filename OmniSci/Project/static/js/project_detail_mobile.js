var now_board = 1;

var board_map = {'submit': 1, 'image': 2, };
var button_board_map = [0, 4, 5];

function changeBoard(next_board)
{
    if (now_board == next_board) {
        return;
    }

    // 修改按钮样式
    document.querySelector("body > div:nth-child(5) > ul > li:nth-child(" + now_board + ") >" +
        " a").classList.remove('active');
    document.querySelector("body > div:nth-child(5) > ul > li:nth-child(" + next_board + ") >" +
        " a").classList.add('active');

    // 修改板块显示
    document.querySelector("body > div:nth-child(5) >" +
        " div:nth-child(" + button_board_map[now_board] + ")").style.display = 'none';
    document.querySelector("body > div:nth-child(5) >" +
        " div:nth-child(" + button_board_map[next_board] + ")").style.display = 'flex';

    now_board = next_board;
}