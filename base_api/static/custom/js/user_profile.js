
const get_info_url = window.location.origin + "/api/user/profile/"
const update_profile_url = window.location.origin + "/api/user/update/"
const create_wallet_url = window.location.origin + "/api/wallet/create_new_wallet/"


var profile_image = null
var profile_image_def = null
var profile_image_reset = false

const email_input = $("#email_input")
const username_input = $("#username_input")
var username_basic = $("#username_basic")
const avatar_basic = $("#avatar_basic")
const avatar_profile = $("#avatar_profile")
const avatar_input = $("#avatar_upload")
const password_input = $("#password")
const password2_input = $("#password2")


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
                email_input.val(data.email)
                username_input.val(data.username)
                username_basic.text(data.username)
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

function create_wallet() {
    $.ajax(
        {
            method: "post",
            headers: {
                "Content-Type": "application/json"
            },
            data: '',
            url: create_wallet_url,
            success: function (data) {
                console.log(data)
                // email_input.val(data.email)
                // username_input.val(data.username)
                // username_basic.text(data.username)
                // if (data.avatar) {
                //     avatar_profile.attr("src", data.avatar);
                //     avatar_basic.attr("src", data.avatar);
                // }
            },
            error: function (data) {
                console.log(data)
            }
        },
    )
}

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
                toastr["success"]("Profile have changed successfully", "Success").css("width","500px")

            },
            error: function (data) {
                console.log(data)
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
    // $("#management_file").html(
    //     '<div>\n' +
    //     '    <button type="reset" onclick="backImageUpload(true)" class="btn btn-sm btn-outline-secondary mb-75 waves-effect"> Отменить удаление\n' +
    //     '    </button>\n' +
    //     '</div>'
    // )
}
