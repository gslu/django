function init_viewer(){
      $('#dowebok').viewer({
      url: 'data-original',
      });
  };

$(document).ready(function() {
        /*定位到错误的位置*/
        try{
            $("html,body").animate({scrollTop:$(".errorlist").offset().top},1);
        }
        catch(err)
        {}
    $('#write-form').submit(function() {
        jQuery.ajax({
        url:this.action,
        data:$(this).serialize(),
        type:this.method,
        dataType:"html",
        beforeSend:function()
        {
            $("#save-msg").text("正在保存..");
        },
        success:function(responseText)
        {
            $("#save-msg").text("已保存");
            $("#save-btn").attr("disabled",true);
            $("#see-post").attr("disabled",true);
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
            success:function(responseText)
            {
                $("#save-msg").text("已保存");
                $("#save-btn").attr("disabled",true);
                $("#save-msg").text("已发布");
                $("#publish-btn").attr("disabled",true);
                $("#see-post").attr("disabled",false);
                dom = $(responseText);
                $("#see-post").attr("onclick",dom.find("#see-post").attr("onclick"));
            },
            complete:function(){

            },
            });
            return false;
     });

/*
    $('.nav-ul a').on('click', function(e) {
      e.preventDefault();  // 阻止链接跳转
      var url = this.href;  // 保存点击的地址
      var cls = $(this).attr('class');

      if(url.indexOf("picture") >= 0)
      {
        window.location.href=url;
        return false;
      }

      $("#container").remove();
      $('.nav-ul a').css("color",'#424242');
      $('.'+cls).css("color",'#CD2626');
      $("#tail").load(url + " #container",function(responseTxt,statusTxt,xhr){

            if(statusTxt=="success")
            {
                var dom = $(responseTxt);
                var new_title = dom.filter("title").text();
                document.title = new_title;
                if(history.pushState){
                  var state=({
                    url: url, title:new_title
                    });
                  window.history.pushState(state, new_title, url);
                }
                else
                {
                    window.location.href=url;
                }
            }
            if(statusTxt=="error")
            {
                alert("Error: "+xhr.status+": "+xhr.statusText);
            }
      });

    });
*/

    $('#books a').click(function(e){
        e.preventDefault();
        var url = this.href;
        if(history.pushState){
            var state=({
              url: url, title:''
             });
             window.history.pushState(state, '', url);
        }
        else
        {
           window.location.href=url;
        }

        $.get(url,function(responseText){
            dom = $(responseText)
            //var blctn = dom.find("#blctn").html();
            var tlctn = dom.find("#tlctn").html();
            var plctn = dom.find("#plctn").html();
            var tag_form = dom.find("#new-tag-form").html();
            //$('#blctn').html(blctn);
            $('#tlctn').html(tlctn);
            $('#plctn').html(plctn);
            $('#new-tag-form').html(tag_form);
        });

        $(this).children().addClass("select-book");
        $(this).children().css("background","#8E8E38");
        $(this).siblings().children().removeClass("select-book");
        $(this).siblings().children().css("background","#8B814C");
    });

    $('#tags a').click(function(e){
        e.preventDefault();
        var url = this.href;

        if(history.pushState){
            var state=({
              url: url, title:''
             });
             window.history.pushState(state, '', url);
        }
        else
        {
           window.location.href=url;
        }

        $('#plctn').remove();
        $('#post-list').load(url + ' #plctn');

        $(this).children().addClass("select-tag");
        $(this).children().css("background","#F0E68C");
        $(this).siblings().children().removeClass("select-tag");
        $(this).siblings().children().css("background","#F5FFFA");
    });


    $('#nbf').submit(function() {
        jQuery.ajax({
        url:this.action,
        data:$(this).serialize(),
        type:this.method,
        dataType:"html",
        success:function(responseText)
        {
            var url = $('#nbf').attr('action');
            if(history.pushState){
                var state=({
                  url: url, title:''
                 });
                 window.history.pushState(state, '', url);
            }

            dom = $(responseText)
            var blctn = dom.find("#blctn").html();
            var tlctn = dom.find("#tlctn").html();
            var plctn = dom.find("#plctn").html();

            $('#blctn').html(blctn);
            $('#tlctn').html(tlctn);
            $('#plctn').html(plctn);

            $("#id_book_name").val("");
            $('#new-book-form').hide(200);
        }
        });
        return false;
    });

   $('#ntf').submit(function() {
        jQuery.ajax({
        url:this.action,
        data:$(this).serialize(),
        type:this.method,
        dataType:"html",
        success:function(responseText)
        {
            var url = $('#ntf').attr('action');
            if(history.pushState){
                var state=({
                  url: url, title:''
                 });
                 window.history.pushState(state, '', url);
            }

            dom = $(responseText)
            var tlctn = dom.find("#tlctn").html();
            var plctn = dom.find("#plctn").html();
            $('#tlctn').html(tlctn);
            $('#plctn').html(plctn);

            $("#id_tag_name").val("");
            $('#new-tag-form').hide(200);
        }
        });
        return false;
    });



   $('#id_image').change(function(){
        var file = this.files[0];
        name = file.name;
        size = file.size;
        type = file.type;
        //your validation

        $("#image-form").ajaxSubmit({
            dataType :'json',//返回数据类型
            beforeSend:function(){
                $("#change-image").text("正在上传..");
            },
            success:function(data){
                $("#change-image").text("变更头像");
                if(data.path != "error")
                {
                    $('.user-image img').attr("src",data.path);
                    $("#save-status").text("成功变更头像")
                    $("#save-status").slideToggle(800);
                    $("#save-status").slideToggle(1200);
                }
                else
                {alert("系统异常！");}
            },
            error:function(xhr){
                alert("上传失败！");
            }
        });
    });

   $('#id_bgimg').change(function(){
        var file = this.files[0];
        name = file.name;
        size = file.size;
        type = file.type;
        //your validation

        $("#bgimg-form").ajaxSubmit({
            dataType :'json',//返回数据类型
            beforeSend:function(){
                $("#change-bgimg").text("正在上传..");
            },
            success:function(data){
                $("#change-bgimg").text("变更背景");
                if(data.path != "error")
                {
                    $('.bg-image img').attr("src",data.path);
                    $("#save-status").text("成功变更背景")
                    $("#save-status").slideToggle(800);
                    $("#save-status").slideToggle(1200);
                }
                else
                {alert("系统异常！");}
            },
            error:function(xhr){
                alert("上传失败！");
            }
        });
    });


    $("#save-setting").click(function(e){

        var url = $(this).parent().attr("action");
        $("#bpc-form").ajaxSubmit({
            dataType :'html',//返回数据类型
            beforeSend:function(){

            },
            success:function(data){
                try {
                    var data=$.parseJSON(data);
                    }
                catch(err)
                {
                    var data = $(data);
                }
                if(data.status == "success")
                {
                    $(".errorlist").remove();
                    $("#save-status").text("成功保存设置");
                    $("#save-status").slideToggle(800);
                    $("#save-status").slideToggle(1200);

                }
                else
                {
                    $("#bpc-form").submit();
                }
            },
            error:function(xhr){
                alert("上传失败！");
            }
        });
    });

   $("#follow-link").click(function(e){
        e.preventDefault();
        var url = this.href;

        $.get(url,function(responseText){
            var item = $("#follow-link").children();
            if(responseText.status == "cancel-follow")
            {
                item.text("+关注");
                item.css("background","#FFFFE0");
            }
            else
            {
                item.text("+关注 √");
                item.css("background","#BCEE68");
            }
        });

        return false;
    });

   $(".column-bar .collect").click(function(e){
        e.preventDefault();
        var url = this.href;

        $.get(url,function(responseText){

            var item = $(".column-bar .collect").children();

            if(responseText.status == "cancel-collect")
            {
                item.attr("title","收藏文章");
                item.removeAttr("style");
                item.attr("id",'collect');
            }
            else
            {
                item.attr("title","取消收藏");
                item.attr("id",'cancel-collect');
                item.css("background","#C0FF3E");
            }
        });

        return false;
    });

  $("#bar-ctn a").click(function(e){
        e.preventDefault();
        var url = this.href;
        $("#bar-ctn div").removeAttr("class");
        $("#bar-ctn li").removeAttr("class");
        var sub = $(this).children();
        sub.addClass("select");

        if(history.pushState){
            var state=({
              url: url, title:''
             });
             window.history.pushState(state, '', url);
        }
        else
        {
           window.location.href=url;
        }

        $.get(url,function(responseText){
            var dom = $(responseText);
            $("#posts-ctn").html(dom.find("#posts-ctn").html());

        });

        return false;
    });


  $("#about-menu a").click(function(e){
        e.preventDefault();
        var url = this.href;
        $("#about-menu div").removeAttr("class");
        var sub = $(this).children();
        sub.addClass("select");

        if(history.pushState){
            var state=({
              url: url, title:''
             });
             window.history.pushState(state, '', url);
        }
        else
        {
           window.location.href=url;
        }

        $.get(url,function(responseText){
            var dom = $(responseText);
            $("#about-row").html(dom.find("#about-row").html());

        });

        return false;
    });



   $("#log-date #year").click(function(){
        var year = $(this).data('year');
        $("#log-date #"+year).slideToggle(100);
     });



});


function httpHtml(){
   var v = document.getElementById("post-body").innerHTML;
   var reg = /(http:\/\/|https:\/\/)((\w|=|\?|\.|\/|&|-)+)/g;
   v = v.replace(reg, "<a target='view_window' href='$1$2'>$1$2</a>").replace(/\n/g,"");
   document.getElementById("post-body").innerHTML = v;
}

function validate_email(field,alerttxt)
{
   with (field)
       {
           apos=value.indexOf("@")
           dotpos=value.lastIndexOf(".")
           if (apos<1||dotpos-apos<2)
           {alert(alerttxt);return false}
           else {return true;}
       }
}

function validate_form(thisform)
{
    with (thisform)
    {
        if (validate_email(email,"Not a valid e-mail address!")==false)
        {email.focus();return false;}
    }
}

window.onscroll = function(){
   var t = document.documentElement.scrollTop || document.body.scrollTop;
   var back_top = document.getElementById("back-top");
   if( t < 300 ) {
        back_top.style.display = "none";
        //$("#tag-bar").removeAttr("style");
       } else {
        back_top.style.display = "inline-block";
        //$("#tag-bar").css("position","fixed");
        //$("#tag-bar").css("top","50px");
       }
}

function add_pv(post_id)
{
    $.post(
       "/add_pv/",
       { post_id: post_id}
       ).success(function(data){

    });
}

function to_top() {
         $("body,html").animate({scrollTop:0}, 200);
         return false;
     }


function to_point_page() {
         var page_number = $(".page-number input").val();
         window.location.href = "?page=" + page_number;
         return true;
     }
