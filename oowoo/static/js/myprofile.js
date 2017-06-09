$(document).ready(function(){
	$('.yeboi').click(function(e){
		
		
		var friend = $(this).parent().text();
		$.post('/deleteFriend/',{'user':username,'friend':friend},function(data){
				$('#friends').html(data['myFriends']);
		});
	});
	$('.noboi').click(function(e){
		
		
		var friend = $(this).parent().text();
		$.post('/acceptFriendRequest/',{'user':username,'friend':friend},function(data){
				$('#requests').html(data['myFriendRequests']);
				$('#friends').html(data['myFriends']);
		});
	});

	$('.wtfboi').click(function(e){
		var friend = $(this).parent().text();
		$.post('/declineFriendRequest/',{'user':username,'friend':friend},function(data){
				$('#requests').html(data['myFriendRequests']);
		});
		
	});

});