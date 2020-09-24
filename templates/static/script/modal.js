$(document).ready(function () {

    $(document).on('click', '[close-button-id]', function (event){
        event.preventDefault();
        var btn_id = $(this).attr("close-button-id");
        var modal = document.getElementById("modal-" + btn_id);
        modal.style.display = 'none';
    });


    $(document).on('click', '[button-id]', function (event){
        event.preventDefault();
        var btn_id = $(this).attr("button-id");
        window.addEventListener('click', outsideClick(event, btn_id));
        var modal = document.getElementById("modal-" + btn_id);
        modal.style.display = 'block';
    });
        
    
    function outsideClick(event, btn_id) {
        event.preventDefault();
        var modal = document.getElementById("modal-" + btn_id);
        console.log(modal);
        if (event.target == modal) {
            console.log(btn_id);
            modal.style.display = 'none';
        }
    }
    

});
