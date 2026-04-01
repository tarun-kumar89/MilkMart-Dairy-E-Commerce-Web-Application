

$(document).on("click", ".plus-cart", function(){
    var id = $(this).attr("pid");
    var quantityElement = $(this).siblings(".quantity");

    $.ajax({
        type: "GET",
        url: "/pluscart/",
        data: { prod_id: id },
        success: function(data){
            quantityElement.text(data.quantity);
            $("#amount").text("Rs " + data.amount);
            $("#totalamount").text("Rs " + data.totalamount);
        }
    });
});


$(document).on("click", ".minus-cart", function(){
    var id = $(this).attr("pid");
    var quantityElement = $(this).siblings(".quantity");

    $.ajax({
        type: "GET",
        url: "/minuscart/",
        data: { prod_id: id },
        success: function(data){
            quantityElement.text(data.quantity);
            $("#amount").text("Rs " + data.amount);
            $("#totalamount").text("Rs " + data.totalamount);
        }
    });
});


$(document).on("click", ".remove-cart", function(){
    var id = $(this).attr("pid");
    var row = $(this).closest(".row");

    $.ajax({
        type: "GET",
        url: "/removecart/",
        data: { prod_id: id },
        success: function(data){
            row.remove();
            $("#amount").text("Rs " + data.amount);
            $("#totalamount").text("Rs " + data.totalamount);
        }
    });
});



// $('.plus-wishlist').click(function(){
//     var id=$(this).attr("pid").toString();
//     $.ajax({
//         type:"GET",
//         url:"/pluswishlist",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             //alert(data.message)
//             window.location.href = `http://localhost:8000/product-detail/${id}`
//         }
//     })
// })


// $('.minus-wishlist').click(function(){
//     var id=$(this).attr("pid").toString();
//     $.ajax({
//         type:"GET",
//         url:"/minuswishlist",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             window.location.href = `http://localhost:8000/product-detail/${id}`
//         }
//     })
// })


// $(document).on('click', '.plus-wishlist', function(){
//     var id = $(this).attr("pid").toString();
//     var eml = this;

//     $.ajax({
//         type: "GET",
//         url: "/pluswishlist/",
//         data: {
//             prod_id: id
//         },
//         success: function(data){
//             $(eml).removeClass("btn-success plus-wishlist")
//                   .addClass("btn-danger minus-wishlist");
//         }
//     });
// });


// $(document).on('click', '.minus-wishlist', function(){
//     var id = $(this).attr("pid").toString();
//     var eml = this;

//     $.ajax({
//         type: "GET",
//         url: "/minuswishlist/",
//         data: {
//             prod_id: id
//         },
//         success: function(data){
//             $(eml).removeClass("btn-danger minus-wishlist")
//                   .addClass("btn-success plus-wishlist");
//         }
//     });
// });

$(document).on('click', '.plus-wishlist', function(){
    var id = $(this).attr("pid");
    var eml = this;

    $.ajax({
        type: "GET",
        url: "/pluswishlist/",
        data: { prod_id: id },
        success: function(data){
            $(eml).removeClass("btn-success plus-wishlist")
                  .addClass("btn-danger minus-wishlist");
        }
    });
});

$(document).on('click', '.minus-wishlist', function(){
    var id = $(this).attr("pid");
    var eml = this;

    $.ajax({
        type: "GET",
        url: "/minuswishlist/",
        data: { prod_id: id },
        success: function(data){
            $(eml).removeClass("btn-danger minus-wishlist")
                  .addClass("btn-success plus-wishlist");
        }
    });
});