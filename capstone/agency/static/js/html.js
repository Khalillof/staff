(($) => {
    //Add text editor
    $('textarea').summernote({
        placeholder: 'Message Body ',
        tabsize: 2,
        height: 300,                 // set editor height
        minHeight: null,             // set minimum height of editor
        maxHeight: null,             // set maximum height of editor
        //focus: true                  // set focus to editable area after initializing summernote
    });

})(jQuery);