// let ws_url = "ws://127.0.0.1"
let ws_url = "ws://164.90.163.166"


const sio = io(ws_url,
    {
        path: '/ws/socket.io',
        autoConnect: false
    });



var currentLocation = window.location;

sio.on("connect", () => {

});

sio.on("disconnect", () => {

});



const user_data = {};

$(window).on('load', function() {
    const current_user_url = window.location.origin + "/api/user/";
    const current_url = window.location.pathname;
    const blank_avatar = "{{ url_for('static', path='/custom/image/blank-avatar.png')}}"

    toastr.options = {
      "closeButton": true,
      "debug": false,
      "newestOnTop": false,
      "progressBar": false,
      "positionClass": "toast-bottom-right",
      "preventDuplicates": false,
      "onclick": null,
      "showDuration": "300",
      "hideDuration": "1000",
      "timeOut": "5000",
      "extendedTimeOut": "1000",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut"
    }

    if (feather) {
        feather.replace({
            width: 14,
            height: 14
        });
    }
    $.ajax({
        url: current_user_url,
        type: 'GET',
        success: function (data) {
            user_data['user_id'] = data.id
            user_data['user_photo'] = data.photo
            user_data['first_name'] = data.first_name
            user_data['last_name'] = data.last_name
            user_data['username'] = data.username
            user_data['email'] = data.email
            user_data['url'] = current_url
            document.querySelector('.user-name').textContent = user_data['username']
            if (data.photo) {
                document.querySelector("#avatar_basic").src =  data.photo;
            }
            if (data.permission.has_chat_access == false){
                $('#chat_li').attr('class', 'nav-item disabled')
            }
            sio.auth = user_data;
            sio.connect();
        },
        error: (error) => {
            if (error.status == 400){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error').css("width","300px")

            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
            if (error.status == 429){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error').css("width","300px")

            }
        }
    })
})


sio.on("transaction_alert", (data) => {
    if (data.operation === "income") {
        if (data.result === true) {
            let message = "You've just gotten new ETH token to wallet " + data.public_key
            toastr.success("Income transaction", message);
        }
    }
    if (data.operation === "outcome") {
        if (data.result === true) {
            let message = "Your transaction has just sent successfully from wallet - " + data.public_key;
            toastr.success("Outcome transaction", message);
        }
        else if (data.result === false) {
            let message = "Your transaction from " + data.public_key + " was failed."
            toastr.error("Failed", message);
        }
    }
    let balance_to_change = $(`[balance-value=${data.public_key}]`)

    balance_to_change.text(data.current_balance + "ETH");
})

sio.on('open_chat', (data) => {
    toastr.success(data, 'Success').css("width","300px")
    $('#chat_li').attr('class', 'nav-item')
})




