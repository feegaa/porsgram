$(document).ready(function(){

    $('#tags').select2({
        tags: true,
        tokenSeprators: ['.', ' '],
        maximumSelectionLength: 3,
    })

    if($('#is_answered').length) {
        var content = CKEDITOR.instances['id_content'];
        content.on('contentDom', function(event){
            content.on('change', function(event){
                console.log(this.getData());
                document.getElementById('preview').innerHTML = this.getData();
            });
        });        
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
        
        


});