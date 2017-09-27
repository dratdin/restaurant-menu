$(function () {
  console.log("Hello!");
  $('.cart-add').click(function() {
    var url = $(this).attr("data-url");
    console.log(url);
    function success(data) {
      $('.current-cart-count').html(data.current_cart_size);
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

  $('.cart-remove').click(function() {
    var button = $(this);
    var url = button.attr("data-url");
    console.log(url);
    function success(data) {
      if(data.current_cart_size != null)
        $('.current-cart-count').html(data.current_cart_size);
      button.closest(".cart-product").remove();
    };
    function error() {
      alert('Error: item was not removed!');
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
