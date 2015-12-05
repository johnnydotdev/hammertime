$(".choice").on("click", function() {
    event.preventDefault();
    var question_id = $(this).attr("question_id");
    var choice_text = $(this).text();

    if (window[question_id].answer === choice_text) {
        $(this).addClass("pure-button-primary");
    }
});

function formatHint(hint_text) {
    return "<b>Hint:</b> " + hint_text;
}

function formatAnswer(ans_text) {
    return "<b>Explanation:</b> " + ans_text;
}

$(".hint-button").on("click", function() {
    event.preventDefault();
    var question_id = $(this).attr("question_id");
    var hint_id = "#hint" + question_id;
    $(hint_id).html(formatHint(window[question_id].hint));
});

$(".exp-button").on("click", function() {
    event.preventDefault();
    var question_id = $(this).attr("question_id");
    var exp_id = "#exp" + question_id;
    $(exp_id).html(formatAnswer(window[question_id].explanation));
});
