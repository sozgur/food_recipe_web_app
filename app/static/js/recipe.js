//jQuery time

let current_fs, next_fs, previous_fs; //fieldsets
let left, opacity, scale; //fieldset properties which we will animate
let animating; //flag to prevent quick multi-click glitches

function validate() {
  let notvalid = false;
  $(".recipe-error").html("");

  if ($(".step1").css("display") != "none") {
    if ($("#title").val().length < 5 || $("#title").val().length > 50) {
      notvalid = true;
      $("#title-error").html("Title must be between 5 and 50 characters long!");
    }

    if (!$("#title").val()) {
      notvalid = true;
      $("#title-error").html("Title required!");
    }

    if (!$("#ingredients").val()) {
      notvalid = true;
      $("#ingredients-error").html("Ingredients required!");
    }

    if (!$("#directions").val()) {
      notvalid = true;
      $("#directions-error").html("Directions required!");
    }
  }

  if ($(".step2").css("display") != "none") {
    if ($("#prep").val() === "Choose") {
      notvalid = true;
      $("#prep-error").html("Choose preparation time!");
    }

    if ($("#cook").val() === "Choose") {
      notvalid = true;
      $("#cook-error").html("Choose cooking time!");
    }

    if (
      !$("#servings").val() ||
      $("#servings").val() > 16 ||
      $("#servings").val() < 0
    ) {
      notvalid = true;
      $("#servings-error").html("Enter a valid interger!");
    }
  }

  return notvalid;
}

// console.log($(this).parent());

$(".next").click(function () {
  const notvalid = validate();
  if (notvalid || animating) return false;
  animating = true;

  current_fs = $(this).parent();
  next_fs = $(this).parent().next();

  //show the next fieldset
  next_fs.show();
  //hide the current fieldset with style
  current_fs.animate(
    { opacity: 0 },
    {
      step: function (now, mx) {
        //as the opacity of current_fs reduces to 0 - stored in "now"
        //1. scale current_fs down to 80%
        scale = 1 - (1 - now) * 0.2;
        //2. bring next_fs from the right(50%)
        left = now * 50 + "%";
        //3. increase opacity of next_fs to 1 as it moves in
        opacity = 1 - now;
        current_fs.css({
          transform: "scale(" + scale + ")",
          position: "absolute",
        });
        next_fs.css({ left: left, opacity: opacity });
      },
      duration: 800,
      complete: function () {
        current_fs.hide();
        animating = false;
      },
      //this comes from the custom easing plugin
      easing: "easeInOutBack",
    }
  );
});

$(".previous").click(function () {
  if (animating) return false;
  animating = true;

  current_fs = $(this).parent();
  previous_fs = $(this).parent().prev();

  //show the previous fieldset
  previous_fs.show();
  //hide the current fieldset with style
  current_fs.animate(
    { opacity: 0 },
    {
      step: function (now, mx) {
        //as the opacity of current_fs reduces to 0 - stored in "now"
        //1. scale previous_fs from 80% to 100%
        scale = 0.8 + (1 - now) * 0.2;
        //2. take current_fs to the right(50%) - from 0%
        left = (1 - now) * 50 + "%";
        //3. increase opacity of previous_fs to 1 as it moves in
        opacity = 1 - now;
        current_fs.css({ left: left });
        previous_fs.css({
          transform: "scale(" + scale + ")",
          opacity: opacity,
        });
      },
      duration: 800,
      complete: function () {
        current_fs.hide();
        animating = false;
      },
      //this comes from the custom easing plugin
      easing: "easeInOutBack",
    }
  );
});
