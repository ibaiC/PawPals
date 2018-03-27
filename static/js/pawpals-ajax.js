function get_reviews(view_url, dog_slug) {
	
	$("review_block").toggle();
	$.ajax({
		 url: view_url,
		 data: {"dog_slug" : dog_slug},
		 success: function(result){
			print_reviews(result);
		}
	 });
}


function print_reviews(reviews) {
    var out = "";
	var review_list = reviews.reviews;
    var i;

    if (review_list.length != 0) {
    	console.log("yes");
        out += "<table style = 'width:100%;'>";
        out += "<tr>";
        out += "<th></th>";
        out += "<th>User</th>";
        out += "<th>Message</th>";
        out += "<th>Difficulty Rating</th>";
        out += "<th>Date</th>";
        out += "</tr>";
    	
    	for(i = 0; i < review_list.length; i++) {
        	out += "<tr>"
        	out += "<td><img class='rectangle center-cropped' src='/media/" + review_list[i].profile_picture + "' alt='Generic placeholder image' width='200' height='200'></td>";
        	out += "<td>" + review_list[i].username + "</td>";
        	out += "<td>" + review_list[i].comment + "</td>";
        	out += "<td>" + review_list[i].rating + "</td>";
        	out += "<td>" + review_list[i].date + "</td>";
        	out += "</tr>";
        }
    	
    	out += "</table>";
    	
    } else {
    	out += "No reviews to show!";
    }

    document.getElementById("review_block").innerHTML = out;
}





