const get_user_wallets_url = window.location.origin + '/api/wallet/get_user_wallets'
const create_product_url = window.location.origin + '/api/ibay/create_product'
const get_products_url = window.location.origin + '/api/ibay/products'
let image = null
const post_order_url = window.location.origin + '/api/ibay/create-order'
let order_id = null
const get_user_orders_url = window.location.origin + '/api/ibay/orders'

$(document).ready(function() {
    //get all products when page is loaded
    $.ajax({
        url: get_products_url,
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        success: function (data) {
            if(data.length < 1) {
                document.getElementById('no_products').style.display = 'block';
            }
            for (let prop in data) {
                let product = data[prop]
                let class_image = '<div class="col-lg-2 col-sm-2 col-12"><img src="'+ product.image +'" height="100" style="margin-left: -8px"></div>'
                let class_main = '<div class="col-lg-10 col-sm-10 col-12"><div class="row">' +
                    '<div class="col-lg-3 col-md-2 col-4"><p>Title:</p></div>' +
                    '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><p>' +
                    product.title + '</p></div>'+
                    '<div class="col-lg-3 col-md-2 col-4"><p>Address:</p></div>' +
                    '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><u style="color: darkblue">' +
                    product.wallet.publicKey + '</u></div></div><div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Price:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
                    '<p style="font-weight: bold;">' + product.price + 'ETH</p></div></div></div>'+
                    '<div class="demo-inline-spacing"><button type="button" ' +
                    'class="btn btn-primary waves-effect waves-float waves-light" style="font-size: big; width: 150px"' +
                    ' data-bs-toggle="modal" data-bs-target="#BuyProduct" onclick="set_order_id('+ "'" + product.id + "'" +')">Buy</button>' +
                    '</div>'
                let class_block = '<div class="col-lg-6"><div class="card"><div class="card-body text-center">' +
                    '<div class="row">' + class_image + class_main + '</div></div></div></div>'
                $('.products').append(class_block)
            }
        },
        error: (error) => {
            if (error.status == 400){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error')
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
            if (error.status == 429){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error').css("width","300px")

            }
        }
    })

    //get user orders
    $.ajax({
        url: get_user_orders_url,
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        success: function (data) {
            if(data.length < 1) {
                document.getElementById('no_orders').style.display = 'block';
            }
            for (let prop in data) {
                let order = data[prop]
                let class_image = '<div class="col-lg-2 col-sm-2 col-12"><img src="'+ order.product.image +'" height="100"></div>'
                let class_main = '<div class="col-lg-10 col-sm-10 col-12"><div class="row">' +
                    '<div class="col-lg-3 col-md-2 col-4"><p>Title:</p></div>' +
                    '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><p>' +
                    order.product.title + '</p></div>'+
                    '<div class="col-lg-3 col-md-2 col-4"><p>Transaction:</p></div>' +
                    '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><u style="color: darkblue">' +
                    order.txn_hash + '</u></div></div><div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Price:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
                    '<p style="font-weight: bold;">' + order.product.price + 'ETH</p></div></div>'+

                    '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Time:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
                    '<p style="font-weight: bold;">' + order.datetime + '</p></div></div>'

                if(order.status == 'NEW') {
                    class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                    '<p style="font-weight: bold; color: orange">' + order.status + '</p></div></div>'
                }
                else if(order.status == 'DELIVERY') {
                    class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                    '<p style="font-weight: bold; color: darkolivegreen">' + order.status + '</p></div></div>'
                }
                else if(order.status == 'COMPLETE') {
                    class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                    '<p style="font-weight: bold; color: green">' + order.status + '</p></div></div>'
                }
                else if(order.status == 'FAILED') {
                    class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                    '<p style="font-weight: bold; color: darkblue">' + order.status + '</p></div></div>'
                }
                else if(order.status == 'RETURN') {
                    class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                    '<p style="font-weight: bold; color: red">' + order.status + '</p></div></div>'
                }

                if(order.txn_hash_return){
                    class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Refund:</p></div><div class="col-lg-9 col-md-10 col-8 " style="text-align: left">' +
                    '<p class="returning-tnx" style="font-weight: bold;">' + order.txn_hash_return + '</p></div></div></div>'
                }
                else {
                    class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                    '<p>Refund:</p></div><div class="col-lg-9 col-md-10 col-8 " style="text-align: left">' +
                    '<p class="returning-tnx" style="font-weight: bold;">' + '' + '</p></div></div></div>'
                }
                let class_block = '<div class="col-lg-6" id="'+ order.id +'"><div class="card"><div class="card-body text-center">' +
                    '<div class="row">' + class_image + class_main + '</div></div></div></div>'
                $('.orders').append(class_block)
            }
        },
        error: (error) => {
            if (error.status == 400){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error')
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
            if (error.status == 429){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error').css("width","300px")

            }
        }
    })

    //get user wallets for modal selectors
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
                $('#modal_buy_wallet').append(option_block)

            }
        },
        error: (error) => {
            if (error.status == 400){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error').css("width","300px")
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
            if (error.status == 429){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error').css("width","300px")

            }
        }
    })
})


//function for show image in modal
$('#modal_image').on('change', function (event) {
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


//function for delete image in product create modal
$(function() {
     $(document).on('click', '.delete_preview_image', function(){
        $('.preview_image')[0].innerHTML = '';
        image = null
    })
})


//function for create_product request on the server
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
        },
        error: (error) => {
            if (error.status == 400) {
                let error_text = error.responseJSON.detail[0]
                if (error_text.code == 'image_format_error'){
                    toastr.error(error_text.message, 'Error').css("width","500px")
                }
                if (error_text.code == 'remote_space_error'){
                    toastr.error(error_text.message, 'Error').css("width","500px")
                }
                if (error_text.code == 'Wallet undefined') {
                    toastr.error(error_text.message, 'Error')
                }
            }
            if (error.status == 422) {
                let error_text = error.responseJSON[0]
                if (error_text.code == 'validation-error') {
                    toastr.error(error_text.message, 'Error')
                }
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
            if (error.status == 429){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error').css("width","300px")

            }
        }
    })
}

//function for clear create product modal
function open_modal(){
    $('.preview_image')[0].innerHTML = '';
    image = null
    $('#modal_title').val('')
    $('#modal_price').val('')
}

//function for set id of product what will be bought
function set_order_id(id){
    console.log(id)
    order_id = id
}

//function for send buy request on the server
function buy_product(){
    let from_wallet = $('#modal_buy_wallet').find(":selected").val()
    $.ajax({
        url: post_order_url,
        type: 'POST',
        dataType: "json",
        headers: {
            'Content-Type': 'application/json',
        },
        data: JSON.stringify({
            "product_id": order_id,
            "from_wallet": from_wallet
        }),
        success: function (data) {
        },
        error: (error) => {
            if (error.status == 400) {
                let error_text = error.responseJSON.detail[0]
                if (error_text.code == 'Wallet is not defined') {
                    toastr.error(error_text.message, 'Error').css("width","300px")
                }
                if (error_text.code == 'Product undefined') {
                    toastr.error(error_text.message, 'Error').css("width","300px")
                }
                else{
                    toastr.error(error_text.message, 'Error').css("width","300px")
                }
            }
             if (error.status == 422) {
                let error_text = error.responseJSON[0]
                if (error_text.code == 'validation-error') {
                    toastr.error(error_text.message, 'Error').css("width","300px")
                }
            }
            if (error.status == 403 || error.status == 401) {
                document.location.reload();
            }
            if (error.status == 429){
                let error_text = error.responseJSON.detail[0]
                toastr.error(error_text.message, 'Error').css("width","300px")

            }
        }
    })
}

// socketio show new products
sio.on("show_new_product", (data) => {
    console.log(data)
    if(document.getElementById('no_products')){
        let parents = document.getElementById('no_products').parentNode;
        parents.remove();
    }
    let class_image = '<div class="col-lg-2 col-sm-2 col-12"><img src="'+ data.image +'" height="100"></div>'
    let class_main = '<div class="col-lg-10 col-sm-10 col-12"><div class="row">' +
        '<div class="col-lg-3 col-md-2 col-4"><p>Title:</p></div>' +
        '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><p>' +
        data.title + '</p></div>'+
        '<div class="col-lg-3 col-md-2 col-4"><p>Address:</p></div>' +
        '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><u style="color: darkblue">' +
        data.address + '</u></div></div><div class="row"><div class="col-lg-3 col-md-2 col-4">' +
        '<p>Price:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
        '<p style="font-weight: bold;">' + data.price + 'ETH</p></div></div></div>'+
        '<div class="demo-inline-spacing"><button type="button" ' +
        'class="btn btn-primary waves-effect waves-float waves-light" style="font-size: big; width: 150px"' +
        ' data-bs-toggle="modal" data-bs-target="#BuyProduct"  onclick="set_order_id('+ "'" + data.id + "'" +')">Buy</button>' +
        '</div>'
    let class_block = '<div class="col-lg-6"><div class="card"><div class="card-body text-center">' +
        '<div class="row">' + class_image + class_main + '</div></div></div></div>'
    $('.products').prepend(class_block)
})

//socketio show new order
sio.on('new_order_show', (data) => {
    if(document.getElementById('no_orders')){
        let parents = document.getElementById('no_orders').parentNode;
        parents.remove();
    }
    let class_image = '<div class="col-lg-2 col-sm-2 col-12"><img src="'+ data.product.image +'" height="100"></div>'
    let class_main = '<div class="col-lg-10 col-sm-10 col-12"><div class="row">' +
        '<div class="col-lg-3 col-md-2 col-4"><p>Title:</p></div>' +
        '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><p>' +
        data.product.title + '</p></div>'+
        '<div class="col-lg-3 col-md-2 col-4"><p>Transaction:</p></div>' +
        '<div class="col-lg-9 col-md-10 col-8" style="text-align: left"><u style="color: darkblue">' +
        data.txn_hash + '</u></div></div><div class="row"><div class="col-lg-3 col-md-2 col-4">' +
        '<p>Price:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
        '<p style="font-weight: bold;">' + data.product.price + 'ETH</p></div></div>'+

        '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
        '<p>Time:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
        '<p style="font-weight: bold;">' + data.datetime + '</p></div></div>'
        if(data.status == 'NEW') {
            class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                '<p class="" style="font-weight: bold; color: orange">' + data.status + '</p></div></div>'
        }
        else if(data.status == 'DELIVERY') {
            class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                '<p class="" style="font-weight: bold; color: darkolivegreen">' + data.status + '</p></div></div>'
        }
        else if(data.status == 'COMPLETE') {
            class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                '<p class="order-status" style="font-weight: bold; color: green">' + data.status + '</p></div></div>'
        }
        else if(data.status == 'FAILED') {
            class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                '<p class="order-status" style="font-weight: bold; color: darkblue">' + data.status + '</p></div></div>'
        }
        else if(data.status == 'RETURN') {
            class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
                '<p>Status:</p></div><div class="col-lg-9 col-md-10 col-8 status-order" style="text-align: left">' +
                '<p class="order-status" style="font-weight: bold; color: red">' + data.status + '</p></div></div>'
        }
    if(data.txn_hash_return){
        class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
            '<p>Refund:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
            '<p class="returning-tnx" style="font-weight: bold;">' + data.txn_hash_return + '</p></div></div></div>'
    }
    else {
        class_main += '<div class="row"><div class="col-lg-3 col-md-2 col-4">' +
            '<p>Refund:</p></div><div class="col-lg-9 col-md-10 col-8" style="text-align: left">' +
            '<p class="returning-tnx" style="font-weight: bold;">' + '' + '</p></div></div></div>'
    }
    let class_block = '<div class="col-lg-6" id="'+ data.id + '"><div class="card"><div class="card-body text-center">' +
        '<div class="row">' + class_image + class_main + '</div></div></div></div>'
    $('.orders').prepend(class_block)
})


function change_status(status) {
    var class_main = ""
    if(status == 'NEW') {
            class_main = '<p class="order-status" style="font-weight: bold; color: orange">' + status + '</p>'
        }
        else if(status == 'DELIVERY') {
            class_main = '<p class="order-status" style="font-weight: bold; color: darkolivegreen">' + status + '</p>'
        }
        else if(status == 'COMPLETE') {
            class_main += '<p class="order-status" style="font-weight: bold; color: green">' + status + '</p>'
        }
        else if(status == 'FAILED') {
            class_main += '<p class="order-status" style="font-weight: bold; color: darkblue">' + status + '</p>'
        }
        else if(status == 'RETURN') {
            class_main +=  '<p class="order-status" style="font-weight: bold; color: red">' + status + '</p>'
        }
        return class_main
}


sio.on('update_order_status', (data) => {
    var ids = `#${data.order_id}`
    var order_block = $(ids)
    var status_order = order_block.find(".status-order")
    let status_block = change_status(data.status)
    status_order.html(status_block)
    if (data.returning_txn) {
        var returning_tnx = order_block.find(".returning-tnx")
        returning_tnx.text(data.returning_txn)
    }
})

