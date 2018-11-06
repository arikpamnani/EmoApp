function change_hw(id, val) {
	$("#"+id).height(val);
	$("#"+id).width(val);
}


$(document).ready(function() {
	$("#turn_1").val("I am in love!");
	$("#turn_2").val("with whom???");
	$("#turn_3").val("with NLP");

	$("#analyze").click(function(e) {
		e.preventDefault();

		$("#analyze").html("Loading...");

		change_hw("others", "80px");
		change_hw("happy", "80px");
		change_hw("sad", "80px");
		change_hw("angry", "80px");

		var conversation = {
			turn_1: $("#turn_1").val(),
			turn_2: $("#turn_2").val(),
			turn_3: $("#turn_3").val()
		}

		$.ajax({
			type: "POST",
			url: "/app",
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify(conversation),
			success: function(response) {
				change_hw(response["emotion"], "120px");
				$("#analyze").html("Analyze");
			}
		});
	});
});
