$(function(){
            toolbar = [ 'title', 'bold', 'italic', 'underline', 'strikethrough',
                        'color', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|',
                        'link', 'image', 'hr', '|', 'indent', 'outdent' ];
            var editor = new Simditor( {
                textarea : $('#id_body'),
                placeholder : '文章内容...',
                toolbar : toolbar,  //工具栏
                defaultImage : "static/blog/simditor/images/image.png",//'{% static "blog/simditor/images/image.png" %}', //编辑器插入图片时使用的默认图片
                upload : {
                    url : "/upload/",//'{% url "blog:upload_image" %}', //文件上传的接口地址
                    params: null, //键值对,指定文件上传接口的额外参数,上传的时候随文件一起提交
                    fileKey: 'fileData', //服务器端获取文件数据的参数名
                    connectionCount: 3,
                    leaveConfirm: '正在上传文件'
                }
            });
          })
