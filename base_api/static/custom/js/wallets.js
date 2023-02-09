const get_wallets_url = window.location.origin + '/api/wallet/get_user_wallets'
const get_transaction_create_url = window.location.origin + '/api/wallet/send_transaction'
let from_address = ''


$(document).ready(function() {
    $.ajax({
        url: get_wallets_url,
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        success: function (data) {
            console.log('success return data = ', data.length)
            if(data.length < 1) {
                document.getElementById('no_wallets').style.display = 'block';
            }
            for (let prop in data) {
                let wallet_data = data[prop]
                let class_image = '<div class="col-lg-2 col-sm-2 col-12"><img src="'+ eth_avatar +'" height="100"></div>'
                let class_main = '<div class="col-lg-10 col-sm-10 col-12"><div class="row">' +
                    '<div class="col-lg-3 col-md-2 col-4"><p>Address:</p></div>' +
                    '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><u style="color: darkblue">' +
                    wallet_data.public_key + '</u></div></div><div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Balance:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
                    '<p style="font-weight: bold;">' + wallet_data.balance + 'ETH</p></div></div>' +
                    '<div class="demo-inline-spacing"><button type="button" class="btn btn-primary waves-effect waves-float waves-light" style="font-size: small">Watch Transactions</button>' +
                    '<button type="button" class="btn btn-success waves-effect waves-float waves-light send" style="font-size: small" value="'
                    + wallet_data.public_key + '" data-bs-toggle="modal" data-bs-target="#addNewCard" onclick="open_modal()">Send Transaction</button>' +
                    '<button type="button" class="btn btn-warning waves-effect waves-float waves-light" style="font-size: small"' +
                    'data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="1. Go to Web service &#10;' +
                    '2. Make tweet with you wallet number &#10;' +
                    '3. Copy your tweet url &#10;' +
                    '4. Past url to field on web service &#10;' +
                    '5. Press button «Send Me ETH»"' +
                    'onclick="window.location.href = \'https://faucet-sepolia.rockx.com/\';">Get Free ETH</button>' +
                    '</div></div>'
                let class_block = '<div class="col-lg-6"><div class="card"><div class="card-body text-center">' +
                    '<div class="row">' + class_image + class_main + '</div></div></div></div>'
                $('.wallets').append(class_block)

            }
        },
        error: (error) => {
            console.log('error get')
            if (error.status == 400){
                let error_text = error.responseJSON.detail[0]
                if (error_text.code == 'Web3 error'){
                    toastr.error(error_text.message, 'Error')
                }
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
        }
    })
})

document.addEventListener('click', function(e) {
  if (e.target.classList.contains('send')) {
      console.log(e.target.value)
      from_address = e.target.value
  }
});

function open_modal(){
    $('#modal_address').val('')
    $('#modal_value').val('')
}


function send_transaction(){
    let to_address = $('#modal_address').val()
    let amount = $('#modal_value').val()
    console.log(to_address, amount)
    if (!to_address || !amount){
        toastr.error('Field "Send To" or "Value" is empty', "Empty field").css("width","300px")
    }
    else {
        $.ajax({
            url: get_transaction_create_url,
            type: 'POST',
            dataType: "json",
            headers: {
                'Content-Type': 'application/json',
            },
            data: JSON.stringify({
                "from_address": from_address,
                "to_address": to_address,
                "amount": amount
            }),
            success: function (data) {
                console.log(data.url)
                toastr.success('Create new transaction <a href="' + data.url + '" target="_blank" style="color: darkblue">Transaction URL</a>' , 'Success').css("width", "300px")
                // document.getElementById('no_wallets').style.display = 'none';
                // let image = '<img src="' + eth_avatar + '" alt="ETH" width="70px" height="50px">'
                // let wallet = '<span class="wallet_number">' + data.public_key + '</span>'
                // let block = '<div class="col-12 ethereum-wallet">' + image + wallet + '</div>'
                // $('.wallets').append(block)
            },
            error: (error) => {
                console.log('import wallet error  ', error)
                if (error.status == 400) {
                    let error_text = error.responseJSON.detail[0]
                    console.log(error_text)
                    if (error_text.code == 'Wallet is not defined') {
                        toastr.error(error_text.message, 'Error').css("width", "300px")
                    }
                    if (error_text.code == 'Transaction error') {
                        toastr.error(error_text.message, 'Error').css("width", "300px")
                    }
                }
                if (error.status == 422) {
                    let error_text = error.responseJSON[0]
                    if (error_text.code == 'validation-error') {
                        toastr.error(error_text.field + ' ' + error_text.message, 'Error').css("width", "300px")
                    }
                }
                if (error.status == 403 || error.status == 401) {
                    document.location.reload();
                }
            }
        })
    }
}


