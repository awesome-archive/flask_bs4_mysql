/**
 * Created by millyn on 16/7/1.
 */
function getcnbeta() {
    $.get("/update/cnbeta", function (result) {
        if (result == 'success') {
            layer.msg('获取成功');
            $('#cnbeta_list').datagrid('reload');
        }
        else if (result == 'time_no') {
            layer.msg('刷新时间未到')
        }
        else if (result == 'init') {
            layer.msg('第一次初始化成功')
        } else {
            layer.msg('出现错误')
        }
    });
}

function getv2ex() {
    $.get("/update/v2ex", function (result) {
        if (result == 'success') {
            //正上方
            layer.msg('获取成功', {
                offset: 0,
                shift: 1
            });
        }
        else if (result == 'time_no') {
            layer.msg('刷新时间未到')
        }
        else if (result == 'init') {
            layer.msg('第一次初始化成功')
        } else {
            layer.msg('出现错误')
        }
    });
}