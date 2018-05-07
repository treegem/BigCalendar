$(document).ready(function() {

    function checkbox_clicked(data){
        document.getElementById(data.other_id).checked = !document.getElementById(data.id).checked;
        window.location.reload(false);
    };

    $(":checkbox").change(function(){

        var id = this.id;
        var checked = document.getElementById(id).checked;
        $.get("checkbox_clicked/" + id + '/' + checked, function(data) {
            checkbox_clicked(data)
        });
    });
});