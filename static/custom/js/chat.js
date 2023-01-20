const message_create_url = window.location.origin + "/api/chat/message_create"


function new_message(source){
    var message = $('.message').val();
    if (/\S/.test(message)) {
        create_message_post(message)
        console.log(message)

    }
    enterChat();
}


function create_message_post(message_text) {
            $.ajax({
                url: message_create_url,
                type: 'POST',
                data: {
                    'text': message_text
                },
                success: function (data) {
                    console.log('success return data = ', data)

                },
                error: (error) => {
                    console.log(error);
                }
            })
        }