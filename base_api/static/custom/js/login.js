
const login_url = window.location.origin + "/api/user/login/"

//login function
function login(){
  var email = $("#email");
  var password = $("#password");
  let error_email = $('#error_email');
  let error_password = $('#error_password')
  let error_empty = $('#error_empty')

  if (!email.val() || !password.val() ) {
    error_empty.text("You should fill in all fields")
    error_empty.css("display", "block")
    return
  }

  $.ajax({
    method: 'post',
    dataType: "json",
    headers: {
      'Content-Type': 'application/json',
    },
    url: login_url,
    data: JSON.stringify({
      "email": email.val(),
      "password": password.val(),
    }),
    success: function(data){
        if (data.access_token) {
        location.reload()
      }
    },
    error: function(data) {
      error_password.css('display', "none")
      error_email.css('display', "none")
      error_empty.text(data.responseJSON.detail)
      error_empty.css("display", "block")
      if (data.status == 429) {
        let error_text = data.responseJSON.detail[0]
        toastr.error(error_text.message, 'Error').css("width", "300px")
      }
    }

  })
}

//function check press login
$("#login_button").click(function() {
  login()
});


//function check press enter
$(document).keydown(function(e) {
    if (e.keyCode === 13) {
      login()
    }
})