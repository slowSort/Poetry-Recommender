//this is on the front end, and gets handled on the back
//by the controller.js express handlers.

$(document).ready(function(){
  $('form').on('submit', function(){
      var item = $('form input');
      var todo = {item: item.val()};
      $.ajax({
        type: 'POST',
        url: '/todo',
        data: todo,
        success: function(data){
          //do something with the data via front-end framework
          location.reload();
        }
      });
      return false;
  });
});
