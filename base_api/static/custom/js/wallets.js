const get_wallets_url = window.location.origin + '/api/wallet/get_user_wallets'



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
                    '<button type="button" class="btn btn-success waves-effect waves-float waves-light" style="font-size: small">Send Transaction</button>' +
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
            // if (error.status == 400){
            //     let error_text = error.responseJSON[0]
            //     if (error_text.code == 'image_format_error'){
            //         toastr.error(error_text.message, 'Error')
            //     }
            //     if (error_text.code == 'remote_space_error'){
            //         toastr.error(error_text.message, 'Error')
            //     }
            // }
            // if (error.status == 403 || error.status == 401) {
            //     document.location.reload();
            // }
        }
    })
})