$(document).ready(function(){
	var room = 0;

	$('.chatRoom').click(function(event){
		var socket = io.connect( 'http://' + document.domain + ':' + location.port )
		socket.emit( 'leave', {'room':room});

		event.preventDefault();
		$('#chat').empty();
		
		room = $(".realChat",this).attr('id');
		
		socket.on( 'connect', function() {
			socket.emit( 'joined', {'room':room});
		});		

		socket.on( 'status', function(data){
			addNotification(data.msg,data.time)
		});
		
		socket.on('send', function(data) {
	    	addSelfMsg(data.msg,data.time);
	  	});

		
		var form = $( '#msgform' ).on( 'submit', function( e ) {
		  e.preventDefault();
		  
		  let user_input = $('#msgsent').val();

		  
		  socket.emit( 'message', {
		    'msg' : user_input,
		    'room' : room
		  } );

		  $( 'input.message' ).val( '' ).focus();
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
		 $("#chat").append('<li><p class="notification">' + msg + '  \
		                	<time>' + time + '</time> \
		                </p></li>');
	};

});





   
