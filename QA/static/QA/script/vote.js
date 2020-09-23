$(document).ready(function(){

    function setQuestionVote(_url, _id, _state) {
        $.ajax({
            url: _url,
            method: "POST",
            acync: true,
            data: {id:_id, state:_state, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() },
            }).done(function(){
                $("#question-counter").load(location.href + " #question-counter")
        });
    }

    function setAnswerVote(_url, _id, _state) {
        $.ajax({
            url: _url,
            acync: true,
            method: "POST",
            data: {id:_id, state:_state, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() },
            }).done(function(){
                $("#answer-"+_id+"-counter").load(location.href + " #answer-"+_id+"-counter")
            });    
    }


    $('#question-vote-up').click(function(event){
        event.preventDefault();
        var is_authenticated = $(this).attr("data-is_authenticated");
        console.log(is_authenticated)
        if(is_authenticated == "True") {
            console.log("sssssssssssss");
            var _url   = $(this).attr("data-href");
            var _id    = $(this).attr("data-question");
            var _state = "True";
            setQuestionVote(_url, _id, _state);
        }
    });
    
    
    $('#question-vote-down').click(function(event){
        event.preventDefault();
        var is_authenticated = $(this).attr("data-is_authenticated");
        if(is_authenticated == "True") {
            console.log("sssssssssssss");
            var _url   = $(this).attr("data-href");
            var _id    = $(this).attr("data-question");
            var _state = "False";
            setQuestionVote(_url, _id, _state);
        }
    });
    
    
    
    // $('#answer-vote-up').click(function(event){
    $(document).on('click', '[element-up-id]', function( event ) {   
        event.preventDefault();
        var is_authenticated = $(this).attr("data-is_authenticated");
        console.log(is_authenticated);
        if(is_authenticated == "True") {
            console.log("sssssssssssss");
            var _url   = $(this).attr("data-href");
            var _id    = $(this).attr("data-answer");
            var _state = "True";
            setAnswerVote(_url, _id, _state)
        }
    });
    
    
    // $('#answer-vote-down').click(function(event){
    $(document).on('click', '[element-down-id]', function( event ) {   
        event.preventDefault();
        var is_authenticated = $(this).attr("data-is_authenticated");
        if(is_authenticated == "True") {
            console.log("sssssssssssss");
            var _url   = $(this).attr("data-href");
            var _id    = $(this).attr("data-answer");
            var _state = "False";
            setAnswerVote(_url, _id, _state)
        }
    });
    
    
    
    
});
