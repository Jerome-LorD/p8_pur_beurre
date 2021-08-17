var get_substitutes = function () {
    $('#save_btn').click(function (e) {
        var selected_products = [];
        $("input:checkbox:checked").each(function () {
            selected_products.push($(this).val());
        });

        $.ajax({
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            type: 'POST',
            url: ajax_url,
            data: JSON.stringify({ "products": selected_products, "ref_product_id": ref_product_id }),
            csrfmiddlewaretoken: '{{ csrf_token }}',

        });
        e.stopImmediatePropagation();
    });
};


// $('input:checkbox').change(function (e) {
//     // $('input:checkbox').on("click", function (e) {
//     // $(document).ready(function (e) {
//     var selected_products = [];

//     $("input:checkbox:checked").each(function () {
//         selected_products.push($(this).val());
//         // 
//     });
//     e.stopImmediatePropagation();

//     $('#save_btn').click(function (event) {
//         $.ajax({
//             contentType: 'application/json; charset=utf-8',
//             dataType: 'json',
//             type: 'POST',
//             url: '/ajax/',
//             data: JSON.stringify({ "products": selected_products, "ref_product_id": ref_product_id }),
//             csrfmiddlewaretoken: csrftoken,
//         });
//         // event.stopImmediatePropagation();
//         // 
//         // event.stopPropagation();

//         console.log(selected_products); // 
//     });

// });

// box-shadow: 2px 0px 16px -4px aliceblue;


// let url = "/ajax";

// async function postJsonData(url, data, headers) {
//     try {
//         const response = await fetch(url, {
//             method: 'POST',
//             body: JSON.stringify(data),
//             headers: headers
//         });
//         return await response.json();

//     } catch (err) {
//         return console.warn(err);
//     }
// }