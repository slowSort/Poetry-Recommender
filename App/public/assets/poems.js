//this is on the front end, and gets handled on the back
//by the controller.js express handlers.

$(document).ready(function(){
  $('button').on('click', function(){
    location.reload();
    /*
      $.ajax({
        type: 'POST',
        url: '/newpoem',
        success: function(){
          location.reload();
        }
      });
      return false;
    */
  });
});
