$(document).ready(function(){
	var room;
	var socket;
	var connected = false;
	$('.chatRoom').click(function(event){
		console.log("hi")
		$('#chat').empty();

		if (connected == false){
			socket = io.connect( 'http://' + document.domain + ':' + location.port )				
			connected = true;
			
		}else{
			socket.emit('leave',{'room':room})
			socket.disconnect()
			socket.socket.connect()	
		}
		event.preventDefault();


		
		room = $(".realChat",this).attr('id');
		


		socket.on( 'connect', function() {
			socket.emit( 'joined', {'room':room});

		});		

		socket.on( 'status', function(data){
			addNotification(data.msg,data.time);
			$('#chat').scrollTop($('#chat')[0].scrollHeight);
		});
		
		socket.on('send', function(data) {
			if (data.username !== username) {	
				addOtherMsg(data.msg,data.time,data.username);
			}else{
				addSelfMsg(data.msg,data.time);
			}
			$('#chat').scrollTop($('#chat')[0].scrollHeight);
	    	
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

		$.post('/getinfo/',{'roomId':room},function(data){
						
			var roomname = data['roomname'];
			var users = data['users'];
			var messages = data['messages'];
			var i,x;
			for (i = 0; i < messages.length; i++){
				x = messages[i];
				user = x['username']
				msg = x['msg']
				time = x['time']
				if (user == username) {
					addSelfMsg(msg,time)
				}else{
					addOtherMsg(msg,time,user)
				}

			}

			$('#title').text(roomname);
			$('#members').text(users);
			
			$("#title").fadeIn(500);
			$("#members").fadeIn(500);

			$("#chat").fadeIn(500);
			
			$("#msgform").fadeIn(500);
			$('#chat').scrollTop($('#chat')[0].scrollHeight);
		});

		
	});

	$('.deleteroom').click(function(e){
		roomId=$(this).parent().prev().attr('id');
		console.log(roomId)
		window.location='http://' + document.domain + ':' + location.port + '/deleteRoom' + roomId;
                          	
	   	e.stopPropagation();
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


});





   
