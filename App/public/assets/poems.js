$(document).ready(function(){
  $('button').on('click', function(){
    var buttonName = this.id; //this id is the buttons name
    var poem_id = $('#poem').data('id') //this id is for the poem
      $.ajax({
        type: 'POST',
        url: '/newpoem',
        data: JSON.stringify({
          buttonName: buttonName,
          poem_id: poem_id
        }),
        contentType: 'application/json; charset=utf-8',
        success: function(poem){
          $('#poem_div').html(poem);
        }
      });
      return false;
  });
});
