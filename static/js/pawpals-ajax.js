function get_reviews(view_url, dog_slug) {
	console.log(dog_slug);
	console.log(view_url);
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
    var out = "<tr>";
	var review_list = reviews.reviews;
    var i;
    for(i = 0; i < review_list.length; i++) {
    	out += "<td><img class='rectangle center-cropped' src='/media/" + review_list[i].profile_picture + "' alt='Generic placeholder image' width='200' height='200'></td>";
    	out += "<td>" + review_list[i].username + "</td>";
    	out += "<td>" + review_list[i].comment + "</td>";
    	out += "<td>" + review_list[i].rating + "</td>";
    	out += "<td>" + review_list[i].date + "</td>";
    }
    out += "</tr>";
    document.getElementById("review_block").innerHTML = out;
}





