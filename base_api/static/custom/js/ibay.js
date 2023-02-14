const get_user_wallets_url = window.location.origin + '/api/wallet/get_user_wallets'
const create_product_url = window.location.origin + '/api/ibay/create_product'
const get_products_url = window.location.origin + '/api/ibay/products'
let image = null
const post_order_url = window.location.origin + '/api/ibay/create-order'

$(document).ready(function() {
    $.ajax({
        url: get_user_wallets_url,
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        success: function (data) {
            if(data.length < 1) {
                document.getElementById('no_wallets').style.display = 'block';
            }
            for (let prop in data) {
                let wallet = data[prop]
                let option_block = '<option value="'+ wallet.public_key +'">' + wallet.public_key + ' (' + wallet.balance + 'ETH)</option>'
                $('#modal_wallet').append(option_block)

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
            "product_id": "891521aa-1c7f-4c7e-8143-5800de599cb1",
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

$('#modal_image').on('change', function (event) {
    console.log('image')
    $('.preview_image')[0].innerHTML = '';
    image = $('#modal_image')[0].files[0];
        if (image) {
            let delete_button = '<button class="delete_preview_image" type="button"><svg data-testid="close-no-outline" fill="none" height="15"' +
                ' viewBox="0 0 24 24" width="15" xmlns="http://www.w3.org/2000/svg">' +
                '<path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="black"></path></svg></button>'

            let preview_image = '<img src="' + URL.createObjectURL(image) + '" alt="' + image.name + '" id="image_preview"' +
                ' style="height: 45px; width: 45px; border-radius: 5px; margin-right: 7px">'

            let preview_image_block = delete_button + preview_image
            $('.preview_image').append(preview_image_block)
        }
})

$(function() {
     $(document).on('click', '.delete_preview_image', function(){
        console.log('click delete')
        $('.preview_image')[0].innerHTML = '';
        image = null
    })
})

function create_product(){
    let data_product = new FormData()
    data_product.append('title', $('#modal_title').val())
    data_product.append('price', $('#modal_price').val())
    data_product.append('address', $('#modal_wallet').find(":selected").val())
    data_product.append('image', image)
    $.ajax({
        url: create_product_url,
        type: 'POST',
        processData: false,
        contentType: false,
        enctype: "multipart/form-data",
        cache: false,
        data: data_product,
        success: function (data) {
            console.log('success return data = ', data)
            let class_image = '<div class="col-lg-2 col-sm-2 col-12"><img src="'+ data.image +'" height="100"></div>'
                let class_main = '<div class="col-lg-10 col-sm-10 col-12"><div class="row">' +
                    '<div class="col-lg-3 col-md-2 col-4"><p>Address:</p></div>' +
                    '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><u style="color: darkblue">' +
                    data.address + '</u></div></div><div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Price:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
                    '<p style="font-weight: bold;">' + data.price + 'ETH</p></div></div></div>'

                let class_block = '<div class="col-lg-6"><div class="card"><div class="card-body text-center">' +
                    '<div class="row">' + class_image + class_main + '</div></div></div></div>'
                $('.wallets').append(class_block)
        },
        error: (error) => {
            console.log('error get')
            console.log(error)
            if (error.status == 400) {
                let error_text = error.responseJSON.detail[0]
                if (error_text.code == 'Web3 error') {
                    toastr.error(error_text.message, 'Error')
                }
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
        }
    })
}