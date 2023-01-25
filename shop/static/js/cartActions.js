$('button[class^="addCart"]').click(function (e) {
  e.preventDefault();
  $.ajax({
    url: "addToCart/" + this.id,
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
    url: "removeFromCart/" + this.id,
    type: "GET",
  }).done((response) => {
    if (response == "success") {
      $(this).parent().remove();
    }
  });
});