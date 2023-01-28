


const login_url = window.location.origin + "/api/user/login/"


$( "#login_button" ).click(function() {
  var email = $("#email");
  var password = $("#password");
  let error_email = $('#error_email');
  let error_password = $('#error_password')
  let error_empty = $('#error_empty')

  if (!email.val() || !password.val() ) {
    console.log("EMPTY")
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
    success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
	     // alert("SUCCESS. TOKEN IN AUTH"); /* В переменной data содержится ответ от index.php. */
        if (data.access_token) {
        location.reload()
      }
      console.log(data)
    },
    error: function(data) {
      error_password.css('display', "none")
      error_email.css('display', "none")
      error_empty.text(data.responseJSON.detail)
      error_empty.css("display", "block")
            }
  })
});
