$(function(){
	
    $("#Pers").click(function(){
        $("#Professional").hide();
        $("#toHide").show();
        $("#shelter_status").val("False");
    });
    
    $("#Prof").click(function(){
        $("#Professional").show();
        $("#toHide").hide();
        $("#shelter_status").val("True")
    });

});

