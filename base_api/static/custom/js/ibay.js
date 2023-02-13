const get_products_url = window.location.origin + '/api/ibay/products'
const post_order_url = window.location.origin + '/api/ibay/create-order'

$(document).ready(function() {
    $.ajax({
        url: get_products_url,
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        success: function (data) {
            console.log('success return data = ', data.length)
            console.log('SUCEES DATA', data)
            if(data.length < 1) {
                document.getElementById('no_wallets').style.display = 'block';
            }
            for (let prop in data) {
                let product_data = data[prop]
                console.log(product_data)
                let class_image = '<div class="col-lg-2 col-sm-2 col-12"><img src="'+ eth_avatar +'" height="100"></div>'
                let class_main = '<div class="col-lg-10 col-sm-10 col-12"><div class="row">' +
                    '<div class="col-lg-3 col-md-2 col-4"><p>Address:</p></div>' +
                    '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><u style="color: darkblue">' +
                    product_data.title + '</u></div></div><div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Balance:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
                    '<p balance-value="'+ product_data.price +'" style="font-weight: bold;">' + product_data.price + 'ETH</p></div></div>' +
                    '<div class="demo-inline-spacing">'+ ' <button type="button" class="btn btn-warning waves-effect waves-float waves-light" style="font-size: small"' +
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
            console.log(error)
            // if (error.status == 400){
            //     let error_text = error.responseJSON.detail[0]
            //     if (error_text.code == 'Web3 error'){
            //         toastr.error(error_text.message, 'Error')
            //     }
            // }
            // if (error.status == 403 || error.status == 401) {
            //     document.location.reload();
            // }
        }
    })
})


$(document).ready(function() {
    $.ajax({
        url: post_order_url,
        type: 'post',
        dataType: "json",
        headers: {
          'Content-Type': 'application/json',
        },
        // processData: false,
        // contentType: false,
        // cache: false,
        data: JSON.stringify({
            "product": "40bf9645-6847-4fcc-a04e-ef63a0feb9c3",
            "from_wallet": "0x7d353a42B7fD1Bb8b2434535D9629f89813F887a"
        }),
        success: function (data) {
            console.log('success return data = ', data.length)
            console.log('SUCEES DATA', data)
        },
        error: (error) => {
            console.log('error get')
            console.log(error)
        }
    })
})
