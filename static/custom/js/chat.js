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



sio.on("get_history", (data) => {
    console.log('get_history')
    // $(data).each(function(index, value) {
    //     console.log(value.text)
    // }
    for (let prop in data) {
        console.log(data[prop])
    }

});


sio.on('get_online_users', (data) => {
    console.log('get_users')
    let user_list_block = $('.chat-users-list')
    $('.online_user').remove()
    console.log(user_list_block)
    let user_list = []
    for (let prop in data) {
        console.log(data[prop].auth)
        auth = data[prop].auth

        let avatar = '<span class="avatar"><img src="' + auth.user_photo + '" height="42" width="42" alt="Generic placeholder image">' +
            '<span class="avatar-status-online"></span>' + '</span>'
        let info = '<div class="chat-info flex-grow-1"><h5 class="mb-0">' + auth.first_name + ' ' + auth.last_name +
        '</h5></div>'
        let li = '<li class="online_user">' + avatar + info + '</li>'
        if (!user_list.includes(auth.user_id)){
            user_list_block.append(li)
        }
        user_list.push(auth.user_id)
    }




})




