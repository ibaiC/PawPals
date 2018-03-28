/** Functions handling AJAX functionality **/

// Get reviews for given dog from database
function get_reviews(view_url, dog_slug, default_user_picture) {
	
	$("review_block").toggle();
	$.ajax({
		 url: view_url,
		 data: {"dog_slug" : dog_slug},
		 success: function(result){
			print_reviews(result, default_user_picture);
		}
	 });
}

// Print reviews to HTML
function print_reviews(reviews, default_user_picture) {
    var out = "";
	var review_list = reviews.reviews;
    var i;

    if (review_list.length != 0) {
        out += "<table style = 'width:100%;'>";
        out += "<tr>";
        out += "<th></th>";
        out += "<th>User</th>";
        out += "<th>Message</th>";
        out += "<th>Difficulty Rating</th>";
        out += "<th>Date</th>";
        out += "</tr>";
    	
    	for(i = 0; i < review_list.length; i++) {
        	out += "<tr>";
        		
        	out += "<td>";        	
        	
        	if (review_list[i].profile_picture) {
                out += "<img class='rectangle center-cropped' src='/media/" + review_list[i].profile_picture + "' alt='Dog image' width='150' height='150'>";

            } else {
                out += "<img class='rectangle center-cropped' src='" + default_user_picture + "' alt='Dog picture' width='150' height='150'>";
            }
        	
        	out += "</td>";
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

//Get dogs from given shelter from database
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

//Print dogs to HTML adhering to grid layout
function print_dogs(dogs, default_picture, dog_profile_url) {
    var out = "";
	var dogs_list = dogs.dogs;
    var i;

    if (dogs_list.length != 0) {

        for(i = 0; i < dogs_list.length; i++) {
        	
            if (i == 0) {
            	// for first open row and print dog
            	out += "<div class='row'>";
	            out += print_dog(dogs_list[i], default_picture, dog_profile_url);
	            
            } else if ( i == (dogs_list.length - 1)) {
            	
            	// for last
            	// create new row if needed, print dog, close row
            	if (i%3 == 0) {
            		out += "</div>";
            		out += "<div class='row'>";
            		out += print_dog(dogs_list[i], default_picture, dog_profile_url);
            		out += "</div>";
            	// if not needed, print dog and close row
            	} else {
            		out += print_dog(dogs_list[i], default_picture, dog_profile_url);
            		out += "</div>";
            	}
	            
            } else {
            	// for any other case other
            	
            	// every third dog, close previous row and open new
            	if (i%3 == 0) {
            		out += "</div>";
	                out += "<div class='row'>";
            	}
            	
            	// print dog
            	out += print_dog(dogs_list[i], default_picture, dog_profile_url);
            }
        }
    } else {
    	out += "No dogs to show!";
    }

    document.getElementById("dogs_block").innerHTML = out;
}

// Print single dog
function print_dog(dog, default_picture, dog_profile_url) {
	var out = "";
	
	// open column
	out += "<div class='col-sm-3'>";
	
	// handle image or lack of
    if (dog.profile_picture) {
        out += "<img class='rectangle center-cropped' src='/media/" + dog.profile_picture + "' alt='Dog picture' width='200' height='200'>";

    } else {
        out += "<img class='rectangle center-cropped' src='" + default_picture + "' alt='Dog picture' width='200' height='200'>";
    }

    // add dog info
    out += "<h3>" + dog.name + "</h3><p>";
    out += "<a class='btn btn-outline-dark' href='" + dog_profile_url + dog.slug + "' role='button'>View dog &raquo;</a>";
    out += "</p>";

    // close column
    out += "</div>";
    
    return out;
    
}
