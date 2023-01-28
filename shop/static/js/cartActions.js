$('button[class^="addCart"]').click(function (e) {
  e.preventDefault();
  $.ajax({
    url: "/addToCart/" + this.id,
    type: "GET",
  }).done((response) => {
    if (response == "success") {
      $(this).prop("disabled", true);
      $(this).html("Added to cart");
    }
  });
});

$('button[name^="removeFromCart"]').click(function (e) {
  e.preventDefault();
  $.ajax({
    url: "/removeFromCart/" + $(this).parent().attr("id"),
    type: "GET",
  }).done((response) => {
    if (response == "success") {
      $(this).parent().remove();
      if ($("div[class^='product']").length == 0) {
        $("#cart").html("Your cart is empty");
        $("#checkoutBtn").remove();
      }
    }
  });
});

$('input[name^="quantity"]').change(function (e) {
  e.preventDefault();
  $.ajax({
    url: "/changeQuantity/" + $(this).parent().attr("id"),
    type: "GET",
    data: { quantity: this.value },
  }).done((response) => {
    if (response == "success") {
      $(this).val(this.value);
    }
  });
});
