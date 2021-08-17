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
            data: JSON.stringify({ "products": selected_products, "user_id": '{{user.id}}', "origin_product": '{{origin_prod_name}}' }),
            csrfmiddlewaretoken: '{{ csrf_token }}',

        });
        e.stopImmediatePropagation();
    });
};