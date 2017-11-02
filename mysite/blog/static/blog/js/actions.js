$(document).ready(function() {

// 使用 jQuery异步提交表单


    $('#write-form').submit(function() {
        jQuery.ajax({
        url:this.action,
        data:$(this).serialize(),
        type:this.method,
        beforeSend:function()
        {
            $("#save-msg").html("正在保存..");
        },
        success:function()
        {
            $("#save-msg").html("已保存");
            $("#save-btn").attr("disabled",true);
        }
        });
        return false;
        });

    $("#write-form :input").change(function(){ $("#save-msg").html("未保存"); });


    $('#publish-btn').click(function(){
            jQuery.ajax({
            url:"./publish/",
            data:$("#write-form").serialize(),
            type:"POST",
            beforeSend:function()
            {
                $("#save-msg").html("正在保存..");
            },
            success:function()
            {
                $("#save-msg").html("已保存");
                $("#save-btn").attr("disabled",true);

            },
            complete:function(){
                $('#publish-btn').val("已发布");
                $("#publish-btn").attr("disabled",true);

            },
            });
            return false;
     });
});

$(document).bind('input propertychange', function(){
        $("#save-msg").html("未保存");
        $('#publish-btn').val("发布");
        $("#publish-btn").attr("disabled",false);
        $("#save-btn").attr("disabled",false);

   });
