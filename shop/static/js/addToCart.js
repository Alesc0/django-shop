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
