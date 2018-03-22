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
    var out = "";
	var review_list = reviews.reviews;
    var i;
    for(i = 0; i < review_list.length; i++) {
        out += "<div class='review'><h4>" + review_list[i].username + "</h4></br>";
        out += "Date: " + review_list[i].date + '</br>';
        out += "How difficult was the walk?: " + review_list[i].rating + "/5</br>";
        out += "Comment: " + review_list[i].comment + "</br>";
        out += "<img class='rectangle center-cropped' src='/media/" + review_list[i].profile_picture + "' alt='Generic placeholder image' width='200' height='200'></div>";

    }
    document.getElementById("review_block").innerHTML = out;
}