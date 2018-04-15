$(document).ready(function() {

    $(":checkbox").change(function(){

        $.post("georg");
        var id = this.id;
        document.write(id);

    });
});