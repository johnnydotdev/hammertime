$(".choice").on("click", function() {
    event.preventDefault();
    var question_id = $(this).attr("question_id");
    var choice_text = $(this).text();

    if (window[question_id].answer === choice_text) {
        alert("YEEEEEEEE");
    }
});
