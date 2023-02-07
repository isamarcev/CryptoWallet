
const get_info_url = window.location.origin + "/api/user/profile/"
const update_profile_url = window.location.origin + "/api/user/update/"
const create_wallet_url = window.location.origin + '/api/wallet/create_new_wallet'
const get_wallets_url = window.location.origin + '/api/wallet/user_wallets'
const import_wallet_url = window.location.origin + '/api/wallet/import_wallet'

var profile_image = null
var profile_image_def = null
var profile_image_reset = false

const email_input = $("#email_input")
const username_input = $("#username_input")
var username_basic = $("#username_basic")
const avatar_basic = $("#avatar_basic")
const avatar_profile = $("#avatar_profile")
const avatar_input = $("#avatar_upload")
const messages_count = $("#messages_count")
const wallets_count = $("#wallets_count")
const password_input = $("#password")
const password2_input = $("#password2")


$(window).on('load', function() {
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
})


function draw_wallets(wallets) {
    let wallets_block = $('.wallets')
    for (let i of wallets) {
        let image = '<img src="'+ eth_avatar +'" alt="ETH" width="70px" height="50px">'
        let wallet = '<span class="wallet_number">'+ i + '</span>'
        let block = '<div class="col-12 ethereum-wallet">' + image + wallet + '</div>'
        wallets_block.append(block)
    }

}


function get_info() {
    $.ajax(
        {
            method: "get",
            headers: {
                "Content-Type": "application/json"
            },
            url: get_info_url,
            success: function (data) {
                console.log(data)
                email_input.val(data.email);
                username_input.val(data.username);
                username_basic.text(data.username);
                messages_count.text(data.messages);
                wallets_count.text(data.wallets.length);
                if (data.wallets.length === 0) {
                    $("#no_wallets").css("dispay", "block")
                } else {
                    draw_wallets(data.wallets)
                }
                if (data.avatar) {
                    avatar_profile.attr("src", data.avatar);
                    avatar_basic.attr("src", data.avatar);
                }
            },
            error: function (data) {
                console.log(data)
            }
        },
    )
}

// function create_wallet() {
//     $.ajax(
//         {
//             method: "post",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             data: '',
//             url: create_wallet_url,
//             success: function (data) {
//                 console.log(data)
//                 // email_input.val(data.email)
//                 // username_input.val(data.username)
//                 // username_basic.text(data.username)
//                 // if (data.avatar) {
//                 //     avatar_profile.attr("src", data.avatar);
//                 //     avatar_basic.attr("src", data.avatar);
//                 // }
//             },
//             error: function (data) {
//                 console.log(data)
//             }
//         },
//     )
//     $.ajax({
//         url: get_wallets_url,
//         type: 'GET',
//         processData: false,
//         contentType: false,
//         cache: false,
//         success: function (data) {
//             console.log('success return data = ', data.length)
//             if(data.length < 1) {
//                 document.getElementById('no_wallets').style.display = 'block';
//             }
//             for (let prop in data) {
//                 let wallet_data = data[prop]
//                 let image = '<img src="' + eth_avatar + '" alt="ETH" width="70px" height="50px">'
//                 let wallet = '<span class="wallet_number">' + wallet_data.public_key + '</span>'
//                 let block = '<div class="col-12 ethereum-wallet">' + image + wallet + '</div>'
//                 $('.wallets').append(block)
//                 wallets_count.text((Number(wallets_count) + 1))
//
//             }
//         },
//         error: (error) => {
//             console.log('error get')
//             // if (error.status == 400){
//             //     let error_text = error.responseJSON[0]
//             //     if (error_text.code == 'image_format_error'){
//             //         toastr.error(error_text.message, 'Error')
//             //     }
//             //     if (error_text.code == 'remote_space_error'){
//             //         toastr.error(error_text.message, 'Error')
//             //     }
//             // }
//             // if (error.status == 403 || error.status == 401) {
//             //     document.location.reload();
//             // }
//         }
//     })
// }

function updateProfile() {
    let form_data = new FormData()
    form_data.append("username", username_input.val())
    form_data.append("password", password_input.val())
    form_data.append("password2", password2_input.val())
    form_data.append("reset", profile_image_reset)
    $("#username_error").text("")
    $("#password_error").text("")
    $("#password2_error").text("")
    if (profile_image) {
        form_data.append("avatar", profile_image)
    }
    $.ajax(
        {
            cache: false,
            contentType: false,
            processData: false,
            method: "PUT",
            enctype: 'multipart/form-data',
            data: form_data,
            url: update_profile_url,
            success: function (data) {
                console.log(data);
                let detail = data.detail;
                username_basic.text(detail.username);
                username_input.val(detail.username);
                console.log(detail);
                password_input.val("");
                password2_input.val("");
                if (detail.avatar) {
                    avatar_basic.attr("src", detail.avatar);
                }
                else if (profile_image_reset) {
                    avatar_basic.attr("src", blank_avatar);
                }

                toastr["success"]("Profile have changed successfully", "Success").css("width","300px")

            },
            error: function (data) {
                console.log(data)
                if (data.status === 400) {
                    toastr.error("Check the data!");
                    return
                }
                let detail = data.responseJSON.detail
                for (let i of detail) {
                    $("#"+ i.field + "_error").text("*" + i.message)
                }
                console.log(data.responseJSON)
                console.log("EROORS")
            }
        },
    )
}


// load preview images
function loadPreviewImage(element) {

    if (element.files[0]) {
        avatar_profile.attr("src", URL.createObjectURL(element.files[0]))
        profile_image = element.files[0];
        profile_image_reset = false
    } else {
        avatar_profile.attr("src", profile_image_def);
        profile_image = null
    }
}



// delete image
function deleteImage() {
    // delete_image = true
    avatar_profile.attr("src",
        blank_avatar);
    profile_image = null;
    profile_image_reset = true;
}


function create_wallet(){
    $.ajax({
        url: create_wallet_url,
        type: 'POST',
        processData: false,
        contentType: false,
        cache: false,
        success: function (data) {
            toastr.success('Import create new wallet', 'Success').css("width","300px")
            document.getElementById('no_wallets').style.display = 'none';
            let image = '<img src="'+ eth_avatar +'" alt="ETH" width="70px" height="50px">'
            let wallet = '<span class="wallet_number">'+ data.public_key + '</span>'
            let block = '<div class="col-12 ethereum-wallet">' + image + wallet + '</div>'
            $('.wallets').append(block)
            wallets_count.text((Number(wallets_count.text()) + 1))
        },
        error: (error) => {
            if (error.status == 400){
                let error_text = error.responseJSON.detail[0]
                if (error_text.code == 'Privet key error'){
                    toastr.error(error_text.message, 'Error').css("width","300px")
                }
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
        }
    })
}

function import_wallet(){
    let key = $('#modal_key')
    if (!key.val()){
        toastr.error('Private Key is empty', "Empty field").css("width","300px")
    }
    else {
        $.ajax({
            url: import_wallet_url,
            type: 'POST',
            dataType: "json",
            headers: {
                'Content-Type': 'application/json',
            },
            data: JSON.stringify({
                "privet_key": key.val()
            }),
            success: function (data) {
                toastr.success('Import new wallet', 'Success').css("width","300px")
                document.getElementById('no_wallets').style.display = 'none';
                let image = '<img src="' + eth_avatar + '" alt="ETH" width="70px" height="50px">'
                let wallet = '<span class="wallet_number">' + data.public_key + '</span>'
                let block = '<div class="col-12 ethereum-wallet">' + image + wallet + '</div>'
                $('.wallets').append(block)
            },
            error: (error) => {
                console.log('import wallet error  ', error)
                if (error.status == 400){
                    let error_text = error.responseJSON.detail[0]
                    console.log(error_text)
                    if (error_text.code == 'Privet key error'){
                        toastr.error(error_text.message, 'Error').css("width","300px")
                    }
                    if (error_text.code == 'Wallet already exists'){
                        toastr.error(error_text.message, 'Error').css("width","300px")
                    }
                }
                if (error.status == 403 || error.status == 401) {
                    document.location.reload();
                }
            }
        })
    }

}

function open_modal(){
    let key = $('#modal_key')
    key.val('')
}