const message_create_url = window.location.origin + "/api/chat/message_create"
let prev_user_new_message = ''

function new_message(source){
    var message = $('.message').val();
    if (/\S/.test(message)) {
        create_message_post(message)
        console.log('message')

    }
    console.log($('.chat:last-child')[0].className)
    let chat_body = $('.chat:last-child')[0]
    let chat_list = $('.chats')
    if (chat_body.className == 'chat'){
        enterChat();
    }
    else {
        // var html = '<div class="chat-content">' + '<p>' + message + '</p>' + '</div>';
        let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
        let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message + '</p></div></div>'
        let chat = '<div class="chat">' + chat_avatar + chat_body + '</div>'
        chat_list.append(chat)
        $('.message').val('');
        $('.user-chats').scrollTop($('.user-chats > .chats').height());
    }
    // let last_chat_body = $('.chat-body').last()
    // enterChat();
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
    console.log(user_data)
    let chat_list = $('.chats')
    let prev_user_message = ''
    for (let prop in data) {
        message = data[prop]
        console.log(data[prop])

        if (prev_user_message !== message.user_id) {
            if (user_data.user_id == message.user_id) {
                let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
                let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message.text + '</p></div></div>'
                let chat = '<div class="chat">' + chat_avatar + chat_body + '</div>'
                chat_list.append(chat)
            }
            else {
                let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
                let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message.text + '</p></div></div>'
                let chat = '<div class="chat chat-left">' + chat_avatar + chat_body + '</div>'
                chat_list.append(chat)
            }
        }
        else {
            console.log('one')
            // if (user_data.user_id == message.user_id) {
                let chat_content = '<div class="chat-content"><p>' + message.text + '</p></div>'
                let last_chat_body = $('.chat-body').last()
                last_chat_body.append(chat_content)
                console.log('last elem = ', $('.chat-body').last())
            // }
            // else {
            //
            // }

        }
        prev_user_message = message.user_id
        prev_user_new_message = prev_user_message
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



sio.on('new_message', (message) => {
    console.log('new test message = ', message)
    let chat_list = $('.chats')
     if (prev_user_new_message !== message.user_id) {
            if (user_data.user_id !== message.user_id) {
               let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
                let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message.text + '</p></div></div>'
                let chat = '<div class="chat chat-left">' + chat_avatar + chat_body + '</div>'
                chat_list.append(chat)
            }
        }
     else {
         console.log('one')
         if (user_data.user_id !== message.user_id) {
             let chat_content = '<div class="chat-content"><p>' + message.text + '</p></div>'
             let last_chat_body = $('.chat-body').last()
             last_chat_body.append(chat_content)
             console.log('last elem = ', $('.chat-body').last())
         }
     }

     prev_user_new_message = message.user_id
})




