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


function get_dogs(shelter_pk, view_url, default_picture, dog_profile_url) {
	
	$("dog_block").toggle();
	$.ajax({
		 url: view_url,
		 data: {"shelter_pk" : shelter_pk},
		 success: function(result){
			print_dogs(result, default_picture, dog_profile_url);
		}
	 });
}

function print_dogs(dogs, default_picture, dog_profile_url) {
    var out = "";
	var dogs_list = dogs.dogs;
    var i;

    if (dogs_list.length != 0) {

        for(i = 0; i < dogs_list.length; i++) {
        	
            if (i == 0) {
            	// for first open both and print
            	out += "<div class='row'>";
	            
	            out += print_dog(dogs_list[i], default_picture, dog_profile_url);
	            
	            console.log("<row>" + dogs_list[i].name);
	            
            } else if ( i == (dogs_list.length - 1)) {
            	
            	
            	// create new row if needed
            	if (i%3 == 0) {
            		out += "</div>";
            		out += "<div class='row'>";
            		out += print_dog(dogs_list[i], default_picture, dog_profile_url);
            		out += "</div>";
            		console.log("</><row>" + dogs_list[i].name + "</>");
            	} else {
            		out += print_dog(dogs_list[i], default_picture, dog_profile_url);
            		out += "</div>";
            		console.log( dogs_list[i].name + "</>");
            	}
	            
            } else {
            	// for other
            	
            	// if every third, close old and open new row
            	if (i%3 == 0) {
            		out += "</div>";
	                out += "<div class='row'>";
	                console.log("</> <row>");
            	}
            	// print
            	out += print_dog(dogs_list[i], default_picture, dog_profile_url);
            	console.log(dogs_list[i].name);
            }
         
        }

    	
    } else {
    	out += "No dogs to show!";
    }

    document.getElementById("dogs_block").innerHTML = out;
}

function print_dog(dog, default_picture, dog_profile_url) {
	// image
	var out = "";
	
	out += "<div class='col-sm-3'>";
	
    if (dog.profile_picture) {
        out += "<img class='rectangle center-cropped' src='/media/" + dog.profile_picture + "' alt='Dog picture' width='200' height='200'>";

    } else {
        out += "<img class='rectangle center-cropped' src='" + default_picture + "' alt='Dog picture' width='200' height='200'>";
    }

    out += "<h3>" + dog.name + "</h3><p>";
    out += "<a class='btn btn-outline-dark' href='" + dog_profile_url + dog.slug + "' role='button'>View dog &raquo;</a>";
    out += "</p>";

    out += "</div>";
    
    return out;
    
}
