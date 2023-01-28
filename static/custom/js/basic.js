let ws_url = "ws://127.0.0.1:8001"

const sio = io(ws_url,
    {
        path: '/ws/socket.io',
        autoConnect: false
    });



var currentLocation = window.location;
console.log(currentLocation)

sio.on("connect", () => {
    console.log('connect_basic')
});

sio.on("disconnect", () => {
    console.log('disconnect')
});




const current_user_url = window.location.origin + "/api/user/"
const current_url = window.location.pathname
let user_data = {}

$(window).on('load', function() {
    const current_user_url = window.location.origin + "/api/user/"
    const current_url = window.location.pathname


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
            console.log('data = ', data)
            user_data['user_id'] = data.id
            user_data['user_photo'] = data.photo
            user_data['first_name'] = data.first_name
            user_data['last_name'] = data.last_name
            user_data['username'] = data.username
            console.log('url = ', current_url)
            user_data['url'] = current_url
            // document.querySelector('.user-name').textContent = user_data['first_name'] + ' ' +  user_data['last_name']
        },
        error: (error) => {
            console.log('error');
        }
    })
    sio.auth = user_data;
    sio.connect();
})
