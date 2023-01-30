//add item to cart
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

//remove item from cart
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
        updateTotal();
      }
    }
  });
});

//change item quantity
$('input[name^="quantity"]').change(function (e) {
  e.preventDefault();
  $.ajax({
    url: "/changeQuantity/" + $(this).parent().attr("id"),
    type: "GET",
    data: { quantity: this.value },
  }).done((response) => {
    if (response == "success") {
      $(this).val(this.value);
      updateTotal();
    }
  });
});

$(document).ready(function () {
  updateTotal();
});

function updateTotal() {
  let total = 0;
  $("*[class=product]").each(function () {
    total += parseFloat(
      $(this).children("input[name='quantity']").val() *
        parseFloat(
          $(this).children("p[id='product-price']").text().slice(0, -1)
        )
    );
  });
  $("#totalprice").text("Total price: " + total.toFixed(2) + "€");
}