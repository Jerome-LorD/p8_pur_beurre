$(function () {
    $("#products").autocomplete({
        minLength: 3,
        source: autocomp_source,
        focus: function (event, ui) {
            $("#products").val(ui.item.name);
            return false;
        },
        select: function (event, ui) {
            $("#products").val(ui.item.name);
            $("#products-id").val(ui.item.value);
            $("#products-icon").attr("src", "{% static '/' %}" + ui.item.icon);
            $(this).closest("form").submit();

            return false;
        }
    })
        .autocomplete("instance")._renderItem = function (ul, item) {
            return $("<li>")
                .append("<div>" + item.name + "</div>")
                .appendTo(ul);
        };

});