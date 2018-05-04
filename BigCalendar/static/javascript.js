$(document).ready(function() {

    function checkbox_clicked(data, id){
        document.getElementById(data.other_id).checked = !document.getElementById(data.id).checked;
        alert(data.id);
    };

    $(":checkbox").change(function(){

        var id = this.id;
        $.get("checkbox_clicked/" + id, function(data, id) {
            checkbox_clicked(data)
        });
    });
});