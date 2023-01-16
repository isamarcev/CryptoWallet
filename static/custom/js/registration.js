

const register_url = window.location.origin + "/api/users/register/"

$( "#register_button" ).click(function() {
  var email = $("#email").val()
  var username = $("#username").val()
  var password = $("#password").val()
  var password2 = $("#password2").val()
  console.log(email)
  console.log(username)
  console.log(password)
  console.log(password2)
  $.ajax({
    method: 'post',
    dataType: "json",
    headers: {
      'Content-Type': 'application/json',
    },
    url: register_url,
    data: JSON.stringify({
      "email": email,
      "username": username,
      "password": password,
      "password2": password2
    }),
    success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
	     alert("SUCCESS. TOKEN IN AUTH"); /* В переменной data содержится ответ от index.php. */

    },
    error: function(data) {
            console.log("error", data.responseJSON.detail);
            alert('error loading from database...');
            }
  })
});