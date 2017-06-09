var socket = io.connect( 'http://' + document.domain + ':' + location.port )

$(document).ready(function(){
	// broadcast a message
	socket.on( 'connect', function() {
		socket.emit( 'joined', {'room':room});
	});	

	socket.on( 'status', function(data){
		$('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
		$('#chat').scrollTop($('#chat')[0].scrollHeight);
	});
	
	socket.on('send', function(data) {
    	$('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

	var form = $( 'form' ).on( 'submit', function( e ) {
	  e.preventDefault();
	  
	  let user_input = $('#msgsent').val();

	  
	  socket.emit( 'message', {
	    'msg' : user_input,
	    'room' : room
	  } );

	  $( 'input.message' ).val( '' ).focus();
	});

	
	var scrolled = false;
	function updateScroll(){
	    if(!scrolled){
	        var element = document.getElementById("chat");
	        element.scrollTop = element.scrollHeight;
	    }
	}

	$("#chat").on('scroll', function(){
	    scrolled=true;
	});	


});
