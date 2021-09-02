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
            csrfmiddlewaretoken: csrftoken,

        });
        e.stopImmediatePropagation();
    });
};