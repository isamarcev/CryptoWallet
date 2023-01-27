const message_create_url = window.location.origin + "/api/chat/message_create"
let prev_user_new_message = ''
let image = null

$('#attach-doc').on('change', function (event) {
   image = $('#attach-doc')[0].files[0];
   console.log('file = ', image)
})

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
    console.log('message_crate image', image)
    let data_message = new FormData()
    data_message.append('text', message_text)
    if (image){
        data_message.append('image', image)
    }
    console.log(data_message)
    $.ajax({
        url: message_create_url,
        type: 'POST',
        processData: false,
        contentType: false,
        enctype: "multipart/form-data",
        cache: false,
        data: data_message,
        success: function (data) {
            console.log('success return data = ', data)
        },
        error: (error) => {
            console.log(error);
            if (error.status == 403) {
                document.location.reload();
            }
        }
    })
}



// $(function() {
//         $(document).on('click', '.online_user', function(){
//             console.log($(this));
//
//             $('.user-profile-sidebar').addClass('show');
//             overlay.addClass('show');
//         });
//     });



function show_user_info(number){
    console.log(number, 'num')
    $('#profile_'+number).addClass('show')
    overlay.addClass('show');
}

overlay.on('click', function () {
      $('.user-profile-sidebar').removeClass('show');
      overlay.removeClass('show');
    });

sio.on("get_history", (data) => {
    console.log('get_history')
    // console.log(user_data)
    let chat_list = $('.chats')
    let prev_user_message = ''
    for (let prop in data) {
        message = data[prop]
        // console.log(data[prop].datetime)

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
            // console.log('one')
            let chat_content = '<div class="chat-content"><p>' + message.text + '</p></div>'
            let last_chat_body = $('.chat-body').last()
            last_chat_body.append(chat_content)
            // console.log('last elem = ', $('.chat-body').last())

        }
        prev_user_message = message.user_id
        prev_user_new_message = prev_user_message
    }

});


sio.on('get_online_users', (data) => {
    console.log('get_users')
    let user_list_block = $('.chat-users-list')
    let content_body = $('.content-body')
    $('.online_user').remove()
    // console.log(user_list_block)
    let user_list = []
    let number = 0
    for (let prop in data) {
        console.log(data[prop].auth)
        auth = data[prop].auth

        let avatar = '<span class="avatar"><img src="' + auth.user_photo + '" height="42" width="42" alt="Generic placeholder image">' +
            '<span class="avatar-status-online"></span>' + '</span>'
        let info = '<div class="chat-info flex-grow-1"><h5 class="mb-0">' + auth.username +
        '</h5></div>'
        let li = '<li class="online_user" onclick="show_user_info('+ number +')">' + avatar + info + '</li>'
        if (!user_list.includes(auth.user_id)){
            user_list_block.append(li)
        }


        let headers = '<header class="user-profile-header"><span class="close-icon">' +
            '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></span>' +
            '<div class="header-profile-sidebar"><div class="avatar box-shadow-1 avatar-border avatar-xl"<img src="' +
            auth.user_photo + '" alt="user_avatar" height="70" width="70"><span class="avatar-status-online avatar-status-lg"></span></div>' +
            '<h4 className="chat-user-name">' + auth.username + '</h4><span class="user-post">👩🏻‍💻</span></div></header>'
        let main_info = '<div class="user-profile-sidebar-area" style="overflow: scroll;"><div class="personal-info">'+
            '<ul class="list-unstyled"><li class="mb-1"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-mail font-medium-2 me-50"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>'+
            '<span class="align-middle">' + auth.email + '</span></li></ul></div>'
        let div = '<div class="user-profile-sidebar" id="profile_' + number + '">' + headers + main_info + '</div>'
        if (!user_list.includes(auth.user_id)){
            content_body.append(div)
        }

        number += 1
        user_list.push(auth.user_id)
    }
})



sio.on('new_message', (message) => {
    // console.log('new test message = ', message)
    let chat_list = $('.chats')
     if (prev_user_new_message !== message.user_id) {
            if (user_data.user_id !== message.user_id) {
               let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
                let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message.text + '</p></div></div>'
                let chat = '<div class="chat chat-left">' + chat_avatar + chat_body + '</div>'
                chat_list.append(chat)
                $('.user-chats').scrollTop($('.user-chats > .chats').height());
            }
        }
     else {
         // console.log('one')
         if (user_data.user_id !== message.user_id) {
             let chat_content = '<div class="chat-content"><p>' + message.text + '</p></div>'
             let last_chat_body = $('.chat-body').last()
             last_chat_body.append(chat_content)
             // console.log('last elem = ', $('.chat-body').last())
             $('.user-chats').scrollTop($('.user-chats > .chats').height());
         }
     }

     prev_user_new_message = message.user_id
})






