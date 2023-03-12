
// send ajax request when transcribe_btn is clicked , pass id

function transcribe_audio(id) {
    $.ajax({
        type: "POST",
        url: "/transcribe",
        data: {
            id: id
        },
        success: function (response) {
            console.log(response);
            if (response.status == "success") {
                // if success, update the text
                $("#transcribe_text").text(response.text);
            }
        }
    });
}



