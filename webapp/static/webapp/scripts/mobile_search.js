$(document).ready(function() {
  $(document).on("click", function() {
    $(".form-input").removeClass("form-input--open");
  });

  $(document).on("click", ".form-input", function(e) {
    e.stopPropagation();
    $(this).addClass("form-input--open").find("input").focus();
  });
});
