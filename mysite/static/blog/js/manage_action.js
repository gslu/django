  $(document).ready(function(){

          function book_rename(book_id,new_name,elem)
          {
            $.post(
            "/book/rename/",
             { book_id: book_id, new_name: new_name }
             ).success(function(data) {
                    elem.text(new_name);
                    });
          }

          function tag_rename(tag_name, book_id, new_name,elem)
          {
            $.post(
            "/tag/rename/",
             { tag_name: tag_name, new_name: new_name,book_id:book_id}

             ).success(function() {
                    elem.text(new_name);
                    var new_url = "/blog/manage/books/"+book_id+"/tags/"+new_name+"/";
                    elem.parent().attr("href",new_url);
                    if(history.pushState){
                        var state=({
                          url: new_url, title:''
                         });
                         window.history.pushState(state, '', new_url);
                    }
                    });
          }

          function book_delete(book_id)
          {
            $.post(
            "/book/delete/",
             { book_id: book_id}
             ).success(function(data) {
                    if(data.status == "error")
                    {
                        alert("专题非空");
                    }
                    else
                    {
                         var new_url = "/blog/manage/";
                         window.location.href=new_url;
                    }
                 });
          }

          function tag_delete(tag_name,book_id)
          {
            $.post(
            "/tag/delete/",
             { tag_name: tag_name,book_id: book_id}
             ).success(function(data) {
                    if(data.status == "error")
                    {
                        alert("标签非空");
                    }
                    else if(data.status == "lastone")
                    {
                        alert("至少需保留一个标签,若不需要可删除空专题");
                    }
                    else
                    {
                         var new_url = "/blog/manage/books/"+book_id+"/";
                         window.location.href=new_url;
                    }
                 });
          }

          function post_delete(post_id, book_id, tag_name)
          {
            $.post(
            "/post/delete/",
             { post_id: post_id}
             ).success(function(data) {
                    if(data.status == "error")
                    {
                        alert("文章不存在,或已删除");
                    }
                    else
                    {
                         var new_url = "/blog/manage/books/"+book_id+"/tags/"+tag_name+"/";
                         window.location.href=new_url;
                    }
                 });
          }

         function change_tag(post_id, book_id, tag_name, new_tag)
          {
            $.post(
            "/post/change_tag/",
             { post_id: post_id,new_tag:new_tag,tag_name:tag_name}
             ).success(function(data) {
                    if(data.status == "error")
                    {
                        alert("文章不存在,或已删除");
                    }
                    else
                    {
                         var new_url = "/blog/manage/books/"+book_id+"/tags/"+new_tag+"/";
                         window.location.href=new_url;
                    }
                 });
          }

          function post_move(post_id,dest_book_id,dest_tag_name)
          {
            $.post(
            "/post/move/",
             { post_id: post_id,dest_book_id:dest_book_id,dest_tag_name:dest_tag_name}
             ).success(function() {
                    alert("second success");
                    });
          }


          $("#new-book-form").hide();
          $("#new-tag-form").hide();
          $(".nb-btn").click(function(){
            $("#new-book-form").slideToggle(500);
          });

          $(".nt-btn").click(function(){
            $("#new-tag-form").slideToggle(500);
          });

        //专题　右击菜单
       var book_menu = new BootstrapMenu('#book', {

          fetchElementData: function($rowElem) {
            return $rowElem;
          },

          actions: [

          　{
              name: '重命名',
              onClick: function(rowElem) {
                var book_id = rowElem.data('bookId');
                var book_name = rowElem.text();
                var new_name = prompt("专题 '" + book_name + "' 重命名为：", "");
                if (new_name != null)
                {
                    new_name = $.trim(new_name);
                    if(new_name == "")
                    {
                        alert("专题名称不能为空");
                    }
                    else
                    {
                        book_rename(book_id,new_name,rowElem);
                    }
                }
              }
            },

            {
              name: '删除空专题',
              onClick: function(rowElem) {
                var book_id = rowElem.data('bookId');
                var book_name = rowElem.text();
                if(confirm("删除空专题: "+book_name)){
                　　book_delete(book_id);
                }
              }
            }]
        });

        //标签　右击菜单
        var tag_menu = new BootstrapMenu('#tag', {

          fetchElementData: function($rowElem) {
            return $rowElem;
          },

          actions: [
          　{
              name: '重命名',
              onClick: function(rowElem) {
                  var tag_name = rowElem.text();
                  var book_id = $(".select-book").data("bookId");
                  var new_name = prompt("标签 '" + tag_name + "' 重命名为：", "");

                  if (new_name != null){
                      new_name = $.trim(new_name);
                      if(new_name == "")
                      {
                         alert("标签名称不能为空");
                      }
                      else
                      {
                          rowElem.text("正在同步文章..请稍等");
                          tag_rename(tag_name,book_id,new_name,rowElem);
                      }

                  }
              }
            },

            {
              name: '删除空标签',
              onClick: function(rowElem) {
                var tag_name = rowElem.text();
                var book_id = $(".select-book").data("bookId");
                if(confirm("删除空标签: "+tag_name)){
                　　 　tag_delete(tag_name,book_id);
                }
              }
            }
            ]
        });

        //文章　右击菜单
        var post_menu = new BootstrapMenu('#post', {

          fetchElementData: function($rowElem) {
            return $rowElem;
          },

          actions: [
            {
              name: '更换标签',
              onClick: function(rowElem) {
                var post_id = rowElem.data('postId');
                var book_id = $(".select-book").data("bookId");
                var tag_name = $(".select-tag").text();
                var new_tag = prompt("由标签'" + tag_name + "' 变更为：", "");
                if(new_tag != null)
                {   new_tag = $.trim(new_tag);
                    if(new_tag == "")
                    {
                        alert("标签名称不能为空");
                    }
                    else
                    {
                        change_tag(post_id, book_id, tag_name, new_tag);
                    }
                }

              }
            },
           // {
            //  name: '移动到',
            //  onClick: function(rowElem) {
            //    var postId = rowElem.data('postId');
            //    alert(postId);
            //  }
           // },

            {
              name: '删除文章',
              onClick: function(rowElem) {
                var post_id = rowElem.data('postId');
                var book_id = $(".select-book").data("bookId");
                var tag_name = $(".select-tag").text();
                var title = rowElem.find("h3").text();
                if(confirm("删除后不可恢复！确认删除\n文章: "+title)){
                　　post_delete(post_id, book_id, tag_name);
                }

              }
            }
           ]
        });
});