$(function(){
      toolbar = [ 'title', 'bold', 'italic', 'underline', 'strikethrough',
                'color', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|',
                'link', 'image', 'hr', '|', 'indent', 'outdent' ];
      var editor = new Simditor( {
          textarea : $('#id_body'),
          placeholder : '文章内容...',
          toolbar : toolbar,
          defaultImage : "static/blog/simditor/images/image.png",
          upload : {
              url : "/upload/",　
              params: null, 　　　
              fileKey: 'fileData',
              connectionCount: 3,
              leaveConfirm: '正在上传文件'
          }
      });
 })

//服务器端获取文件数据的参数名
