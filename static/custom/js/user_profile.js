
const get_info_url = window.location.origin + "/api/user/profile/"

function get_info() {
    let email_input = $("#email_input")
    let username_input = $("#username_input")
    let username_basic = $("#username_basic")
    let avatar_basic = $("#avatar_basic")
    let avatar_profile = $("#avatar_profile")

    $.ajax(
        {
            method: "get",
            headers: {
                "Content-Type": "application/json"
            },
            url: get_info_url,
            success: function (data) {
                console.log("SUCCESS")
                console.log(data)
                email_input.val(data.email)
                username_input.val(data.username)
                username_basic.text(data.username)
            },
            error: function (data) {
                console.log(data)
                console.log("ERRORS")
            }
        },

    )

}