var acceptFriendRequest = function (friend){
	$.ajax({
	  type: "POST",
	  url: "/acceptFriendRequest/",
	  data: { param: friend}
	})
}