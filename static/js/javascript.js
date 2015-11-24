 $(document).scroll(function() {
     //固定SideBar
     if ($(document).scrollTop() > '80') {
         $('.stickup').offset({
             top: $(document).scrollTop() + 5
         });
     } else if ($(document).scrollTop() <= '80') {
         $('.stickup').offset({
             top: $(document).scrollTop() + 68
         });
     };
 });

// function markdown() {
//    var post_text = $('#post-text').html();
//    var opts = {
//        container: 'epiceditor',
//        textarea: 'epiceditor-text',
//        basePath: '../static/epiceditor',
//        clientSideStorage: false,
//        localStorageName: 'epiceditor',
//        useNativeFullscreen: true,
//        parser: marked,
//        file: {
//            name: 'epiceditor',
//            defaultContent: post_text,
//            autoSave: true
//        },
//        theme: {
//            base: '/themes/base/epiceditor.css',
//            preview: '/themes/preview/preview-dark.css',
//            editor: '/themes/editor/epic-dark.css'
//        },
//        button: {
//            preview: true,
//            fullscreen: true,
//            bar: "auto"
//        },
//        focusOnLoad: true,
//        shortcut: {
//            modifier: 18,
//            fullscreen: 70,
//            preview: 80
//        },
//        string: {
//            togglePreview: '预览',
//            toggleEdit: '编辑',
//            toggleFullscreen: '全屏'
//        },
//        autogrow: false
//    };
//
//    //var editor = new EpicEditor().load();
//    var editor = new EpicEditor(opts);
//    editor.load();
//}
//
//$(document).ready(
//    markdown()
//);