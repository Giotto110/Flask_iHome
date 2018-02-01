function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // 在页面加载完毕之后获取区域信息
    $.get("/api/v1.0/areas", function (resp) {
        if (resp.errno == "0") {
            // 代表请求成功
            for (var i = 0; i < resp.data.length; i++) {
                var aid = resp.data[i].aid
                var aname = resp.data[i].aname
                $("#area-id").append('<option value="' + aid + '">' + aname + '</option>')
            }
            var html = template("areas-tmpl", {"areas": resp.data})
            $("#area-id").html(html)
        } else {
            alert(resp.errmsg)
        }
    })

    // 处理房屋基本信息提交的表单数据
    $("#form-house-info").submit(function (e) {
        e.preventDefault()

        var params = {}

        $(this).serializeArray().map(function (x) {
            params[x.name] = x.value
            // console.log(x)
        })
        var facilities = []
        $(":checkbox:checked[name=facility]").each(function (index,x) {
            facilities[index] = x.value
        })
        params["facility"] = facilities
        console.log(params)
        $.ajax({
            url:"/api/v1.0/house",
            type:"post",
            contentType:"application/json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            data:JSON.stringify(params),
            success:function (resp) {
                if (resp.errno == "0"){
                    $("#form-house-info").hide()
                    $("#form-house-image").show()
                }
            }
        })
    })
    // TODO: 处理图片表单的数据

})