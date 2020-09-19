$(document).ready(function(){

    $('#tags').select2({
        tags: true,
        tokenSeprators: ['.', ' '],
        maximumSelectionLength: 3,
    })


    
    if($('#has_editor').length) {
        var content = CKEDITOR.instances['id_content'];
        if (content == null) 
            var content = CKEDITOR.instances['id_about_me'];
        content.on('contentDom', function(event){
            content.on('change', function(event){
                document.getElementById('preview').innerHTML = this.getData();
            });
        });        
    } else {
        $('#pre-view').css('display', 'none');
    }


    $(document).on('click', '[answer-id]', function( event ) {   
        event.preventDefault();
        var likeUrl = $(this).attr("data-href");
        var a_id    = $(this).attr("data-answer-id");
        var aa_id   = $(this).attr("data-answers");
        var flag = true;
        if(aa_id != "False")
            aa_id = aa_id.substring(1, aa_id.length - 1).split(', ');
        else
            flag = false;
        $.ajax({
            url: likeUrl,
            method: "POST",
            data: {answer_id:a_id, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() },
        }).done(function(){
            if(flag != false){
                for(var i=0; i<aa_id.length; i++) 
                    $("#answer-"+aa_id[i]+"-approve").load(location.href + " #answer-"+aa_id[i]+"-approve");
            } else {
                $("#answer-"+a_id+"-approve").load(location.href + " #answer-"+a_id+"-approve");    
            }
        });
    });
        
    setTimeout(function() {
        $('#alert').fadeOut('fast');
    }, 2000);        
    
    


});


$(document).on('click', '[comment-id]', function( event ) {   
    event.preventDefault();

    var ccomment   = document.getElementById('cbox');
    var comment_id = $(this).attr("data-id");
    var each       = document.getElementById('each-'+comment_id);
    var ta_comment = document.getElementById('id-comment-'+comment_id);
    var incbox     = document.getElementById("incbox-"+comment_id);
    initEditTextArea(ta_comment);


    if (incbox.style.display == 'none' || incbox.style.display.length == 0 ) {
        ccomment.style.display = 'none';
        each.style.display     = 'none';   
        incbox.style.display   = 'block';
    }
});
    
$(document).on('click', '[cancel-btn]', function( event ) {   
    event.preventDefault();
    var comment    = document.getElementById('cbox');
    var comment_id = $(this).attr("data-id");
    var incbox     = document.getElementById("incbox-"+comment_id);
    var each       = document.getElementById('each-'+comment_id);

    if (comment.style.display == 'none' || comment.style.display.length == 0 ) {
        comment.style.display = 'block';
        each.style.display    = 'block';   
        incbox.style.display  = 'none';
    }
});

function getComment() {
    var comment  = document.getElementById('comment-box');
    var ccomment = document.getElementById('ccomment');
    console.log(comment.style.display);

    if (comment.style.display == 'none' || comment.style.display.length == 0 ) {
        comment.style.display = 'block';
        ccomment.style.display  = 'none';
        initTextArea();
    }
    else {
        comment.style.display  = 'none';
        ccomment.style.display = 'block';
    }
}


var observe;
if (window.attachEvent) {
    observe = function (element, event, handler) {
        element.attachEvent('on'+event, handler);
    };
}
else {
    observe = function (element, event, handler) {
        element.addEventListener(event, handler, false);
    };
}

function initTextArea () {
    var text = document.getElementById('id_comment');
    function resize () {
        text.style.height = 'auto';
        text.style.height = text.scrollHeight+'px';
    }
    /* 0-timeout to get the already changed text */
    function delayedResize () {
        window.setTimeout(resize, 0);
    }
    observe(text, 'change',  resize);
    observe(text, 'cut',     delayedResize);
    observe(text, 'paste',   delayedResize);
    observe(text, 'drop',    delayedResize);
    observe(text, 'keydown', delayedResize);

    text.focus();
    text.select();
    resize();
}


function initEditTextArea (text) {
    function resize () {
        text.style.height = 'auto';
        text.style.height = text.scrollHeight+'px';
    }
    /* 0-timeout to get the already changed text */
    function delayedResize () {
        window.setTimeout(resize, 0);
    }
    observe(text, 'change',  resize);
    observe(text, 'cut',     delayedResize);
    observe(text, 'paste',   delayedResize);
    observe(text, 'drop',    delayedResize);
    observe(text, 'keydown', delayedResize);

    text.focus();
    text.select();
    resize();
}

