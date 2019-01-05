$(document).ready(function(){
  $('button').on('click', function(){
      $.ajax({
        type: 'POST',
        url: '/newpoem',
        success: function(poem){
          $('#poem').html(poem);
        }
      });
      return false;
  });
});
