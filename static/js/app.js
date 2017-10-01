$(function () {
  console.log("Hello!");
  $('.cart-add').click(function() {
    var url = $(this).attr("data-url");
    console.log(url);
    function success(data) {
      $('.cart__count').html(data.current_cart_count);
      $('.cart__sum').html(data.current_cart_sum);
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
