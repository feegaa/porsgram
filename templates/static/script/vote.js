
 $(document).ready(function(){
   
   $('#question-vote-up').click(function(event){
   event.preventDefault()
   var likeUrl = $(this).attr("data-href")
   var _id     = $(this).attr("data-question")
   var _state  = "True"
   $.ajax({
     url: likeUrl,
     method: "POST",
     data: {id:_id, state:_state, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() },
     }).done(function(){
        $("#question-counter").load(location.href + " #question-counter")
     });
   });


   $('#question-vote-down').click(function(event){
     event.preventDefault()
     var likeUrl = $(this).attr("data-href")
     var _id     = $(this).attr("data-question")
     var _state  = "False"
     $.ajax({
       url: likeUrl,
       method: "POST",
       data: {id:_id, state:_state, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() },
     }).done(function(){
        $("#question-counter").load(location.href + " #question-counter")
     });
   });



   $('#answer-vote-up').click(function(event){
    event.preventDefault()
    var likeUrl = $(this).attr("data-href")
    var _id     = $(this).attr("data-answer")
    var _state  = "True"
    $.ajax({
      url: likeUrl,
      method: "POST",
      data: {id:_id, state:_state, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() },
      }).done(function(){
        $("#answer-counter").load(location.href + " #answer-counter")
      });
    });
 
 
    $('#answer-vote-down').click(function(event){
      event.preventDefault()
      var likeUrl = $(this).attr("data-href")
      var _id     = $(this).attr("data-answer")
      var _state  = "False"
      $.ajax({
        url: likeUrl,
        method: "POST",
        data: {id:_id, state:_state, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() },
      }).done(function(){
        $("#answer-counter").load(location.href + " #answer-counter")
      });
    });


  })

