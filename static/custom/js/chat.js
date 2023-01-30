const message_create_url = window.location.origin + "/api/chat/message_create"
let prev_user_new_message = ''
let image = null

//get image from form
$('#attach-doc').on('change', function (event) {
    $('.preview_image')[0].innerHTML = '';
    image = $('#attach-doc')[0].files[0];
        if (image) {
            let delete_button = '<button class="delete_preview_image" type="button"><svg data-testid="close-no-outline" fill="none" height="15"' +
                ' viewBox="0 0 24 24" width="15" xmlns="http://www.w3.org/2000/svg">' +
                '<path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="black"></path></svg></button>'

            let preview_image = '<img src="' + URL.createObjectURL(image) + '" alt="' + image.name + '" id="image_preview"' +
                ' style="height: 45px; width: 45px; border-radius: 5px; margin-right: 7px">'

            let preview_image_block = delete_button + preview_image
            $('.preview_image').append(preview_image_block)
        }
})

//delete uploaded image
$(function() {
     $(document).on('click', '.delete_preview_image', function(){
        console.log('click delete')
        $('.preview_image')[0].innerHTML = '';
        image = null
    })
})

//post new message
function new_message(source){
    var message = $('.message').val();
    if (/\S/.test(message) || image) {
        if (message.length < 1){
            message = ' '
        }
        create_message_post(message, image)
        image = null
        $('.preview_image')[0].innerHTML = '';
        $('.message').val('');
        $('#attach-doc').val(null);
    }
}

// send message when you press enter
$(document).keydown(function(e) {
    if (e.keyCode === 13) {
        new_message()
    }
})




// send ajax to create message
function create_message_post(message_text, image) {
    // console.log('message_crate image', image)
    let data_message = new FormData()
    data_message.append('text', message_text)
    if (image){
        data_message.append('image', image)
    }
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
            if (error.status == 400){
                let error_text = error.responseJSON[0]
                if (error_text.code == 'image_format_error'){
                    toastr.error(error_text.message, 'Error')
                }
                if (error_text.code == 'remote_space_error'){
                    toastr.error(error_text.message, 'Error')
                }
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
        }
    })
}



//show modal window with user profile info
function show_user_info(number){
    console.log(number, 'num')
    $('#profile_'+number).addClass('show')
    overlay.addClass('show');
}

//hide moda window with user profile info
overlay.on('click', function () {
      $('.user-profile-sidebar').removeClass('show');
      overlay.removeClass('show');
    });

//get message history from server by socketio
sio.on("get_history", (data) => {
    console.log('get_history')
    let chat_list = $('.chats')
    let prev_user_message = ''
    for (let prop in data) {
        message = data[prop]
        if (prev_user_message !== message.user_id) {
            if (user_data.user_id == message.user_id) {
                let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
                if (message.image){
                    let image_chat = '<img src="' + message.image + '" style="width: 100%; height: 150px">'
                    let chat_body = '<div class="chat-body"><div class="chat-content">'+ image_chat +'<p>' + message.text + '</p></div></div>'
                    let chat = '<div class="chat">' + chat_avatar + chat_body + '</div>'
                    chat_list.append(chat)
                }
                else {
                    let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message.text + '</p></div></div>'
                    let chat = '<div class="chat">' + chat_avatar + chat_body + '</div>'
                    chat_list.append(chat)
                }
            }
            else {
                let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
                if (message.image){
                    let image_chat = '<img src="' + message.image + '" style="width: 100%; height: 150px">'
                    let chat_body = '<div class="chat-body"><div class="chat-content">' + image_chat + '<p>' + message.text + '</p></div></div>'
                    let chat = '<div class="chat chat-left">' + chat_avatar + chat_body + '</div>'
                    chat_list.append(chat)
                }
                else {
                    let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message.text + '</p></div></div>'
                    let chat = '<div class="chat chat-left">' + chat_avatar + chat_body + '</div>'
                    chat_list.append(chat)
                }
            }
        }
        else {
            if (message.image){
                let image_chat = '<img src="' + message.image + '" style="width: 100%; height: 150px">'
                let chat_content = '<div class="chat-content">' + image_chat + '<p>' + message.text + '</p></div>'
                let last_chat_body = $('.chat-body').last()
                last_chat_body.append(chat_content)
            }
            else {
                let chat_content = '<div class="chat-content"><p>' + message.text + '</p></div>'
                let last_chat_body = $('.chat-body').last()
                last_chat_body.append(chat_content)
            }
        }
        prev_user_message = message.user_id
        prev_user_new_message = prev_user_message
    }

});

//get online users from server by sockets
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


//get new message from server by socketio
sio.on('new_message', (message) => {
    let chat_list = $('.chats')
     if (prev_user_new_message !== message.user_id) {
            if (user_data.user_id !== message.user_id) {
               let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
                if (message.image){
                    let image_chat = '<img src="' + message.image + '" style="width: 100%; height: 150px">'
                    let chat_body = '<div class="chat-body"><div class="chat-content">' + image_chat +'<p>' + message.text + '</p></div></div>'
                    let chat = '<div class="chat chat-left">' + chat_avatar + chat_body + '</div>'
                    chat_list.append(chat)
                }
                else{
                    let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message.text + '</p></div></div>'
                    let chat = '<div class="chat chat-left">' + chat_avatar + chat_body + '</div>'
                    chat_list.append(chat)
                }
                $('.user-chats').scrollTop($('.user-chats > .chats').height());
            }
            else {
                let chat_avatar = '<div class="chat-avatar"><span class="avatar box-shadow-1 cursor-pointer"><img src="' + '#' +
                    '" alt="avatar" height="36" width="36"></span></div>'
                if (message.image){
                    let image_chat = '<img src="' + message.image + '" style="width: 100%; height: 150px">'
                    let chat_body = '<div class="chat-body"><div class="chat-content">' + image_chat +'<p>' + message.text + '</p></div></div>'
                    let chat = '<div class="chat">' + chat_avatar + chat_body + '</div>'
                    chat_list.append(chat)
                }
                else{
                    let chat_body = '<div class="chat-body"><div class="chat-content"><p>' + message.text + '</p></div></div>'
                    let chat = '<div class="chat">' + chat_avatar + chat_body + '</div>'
                    chat_list.append(chat)
                }
                $('.user-chats').scrollTop($('.user-chats > .chats').height());
            }
        }
     else {
             if (message.image){
                 let image_chat = '<img src="' + message.image + '" style="width: 100%; height: 150px">'
                 let chat_content = '<div class="chat-content">' + image_chat + '<p>' + message.text + '</p></div>'
                 let last_chat_body = $('.chat-body').last()
                 last_chat_body.append(chat_content)
             }
             else {
                 let chat_content = '<div class="chat-content"><p>' + message.text + '</p></div>'
                 let last_chat_body = $('.chat-body').last()
                 last_chat_body.append(chat_content)
             }
             $('.user-chats').scrollTop($('.user-chats > .chats').height());
     }

     prev_user_new_message = message.user_id
})

