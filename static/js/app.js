$(function () {
  console.log("Hello!");

  $.ajax({
    type: 'GET',
    url: 'api/carts/current',
    dataType: 'json',
    success: function(data){
      $('.cart__name').html(data.name);
      $('.cart__count').html(data.count);
      $('.cart__sum').html(data.summary);
    },
    error: function() {
      console.error('Cant load current cart');
    }
  });
  
  $('.cart-add').click(function() {
    var url = $(this).attr("data-url");
    console.log(url);
    function success(data) {
      $('.cart__count').html(data.count);
      $('.cart__sum').html(data.summary);
    };
    function error() {
      alert('Error: item was not added!');
    };
    $.ajax({
      type: 'GET',
      url: url,
      dataType: 'json',
      success: success,
      error: error
    });
  });
});
