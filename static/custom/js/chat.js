function new_message(source){
    var message = $('.message').val();
    if (/\S/.test(message)) {console.log(message)}
    enterChat();
}