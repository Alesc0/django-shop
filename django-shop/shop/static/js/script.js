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
  updateTotalOrders();
});

function updateTotalOrders() {
  $("*[id=order]").each(function () {
    let total = 0;
    $(this)
      .children("*[class=product-order]")
      .each(function () {
        total += parseFloat(
          $(this).children("p[id=product-quantity]").text() *
          parseFloat(
            $(this).children("p[id='product-price']").text().slice(0, -2)
          )
        );
      });
    $(this)
      .children("#totalprice")
      .text("Total price: " + total.toFixed(2) + "€");
  });
}

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

$(document).ready(function () {
  if ($("select[name='type']").val() != 3) {
    el = $("#id_company");
    el.attr("required", false);
    $('label[for="id_company"]').hide()
    $("#id_company").hide()
  }
});

$("select[name='type'").change(function (e) {
  if ($(this).val() == 3) {
    el = $("#id_company");
    el.attr("required", true);
    $('label[for="id_company"]').show()
    $("#id_company").show()
  } else {
    el = $("#id_company");
    el.attr("required", false);
    $('label[for="id_company"]').hide()
    $("#id_company").hide()
  }
});

$("*[name='auth-order']").each(function () {
  $(this).click(function (e) {
    e.preventDefault();
    $.ajax({
      url: "/authorize/" + $(this).attr("id"),
      type: "GET",
    }).done((response) => {
      if (response == "success") {
        text = $(this).closest("details").find('summary').text().replace("awaiting approval", "Authorized")
        $(this).closest("details").find('summary').text(text)
        $(this).remove()
      }
    });
  });
});