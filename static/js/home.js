$(document).ready(function(){
	var room;
	var socket;
	var connected = false;
	$('.chatRoom').click(function(event){
		if (connected == false){
			socket = io.connect( 'http://' + document.domain + ':' + location.port )				
			connected = true;
		}else{
			socket.emit('leave',{'room':room})
			socket = io.reconnect()
		}

		event.preventDefault();
		$('#chat').empty();
		
		room = $(".realChat",this).attr('id');
		
		socket.on( 'connect', function() {
			socket.emit( 'joined', {'room':room});
		});		

		socket.on( 'status', function(data){
			addNotification(data.msg,data.time);
		});
		
		socket.on('send', function(data) {
			console.log(data.username)
			console.log(username)
			if (data.username !== username) {	
				addOtherMsg(data.msg,data.time,data.username);
			}else{
				addSelfMsg(data.msg,data.time);
			}
	    	
	  	});

		$('#msgsent').attr('autocomplete', 'off');
		var form = $( '#msgform' ).on( 'submit', function( e ) {
		  e.preventDefault();
		  
		  let user_input = $('#msgsent').val();

		  
		  socket.emit( 'message', {
		    'msg' : user_input,
		    'room' : room
		  } );

		  $( '#msgsent' ).val( '' ).focus();
		});

	});


	var addSelfMsg = function(msg,time) {
		  $("#chat").append('<li class="self"> \
		                 			 <div class="msg"> \
		                 					   <p>' + msg + '</p> \
		                 					   <time>' + time + '</time> \
		                  		 </div> \
		                		</li>' );
	};

	var addOtherMsg = function(msg,time,user) {
		  $("#chat").append('<li class="other"> \
		                 			 <div class="msg"> \
		                  		    <div class="user">' + user + ' \
		                 					   <p>' + msg + '</p> \
		                 					   <time>' + time + '</time> \
		                  			  </div> \
		                		</li>' );
	};

	var addNotification = function(msg,time){
		 $("#chat").append('<p class="notification">' + msg + '  \
		                	<time>' + time + '</time> \
		                </p>');
	};

	var scrolled = false;
	function updateScroll(){
	    if(!scrolled){
	        var element = $("#right");
	        element.scrollTop = element.scrollHeight;
	    }
	}

	$("#right").on('scroll', function(){
	    scrolled=true;
	});

});





   
