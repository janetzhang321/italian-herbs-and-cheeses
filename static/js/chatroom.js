var socket = io.connect( 'http://localhost:5000/' );

socket.on('connect', function(){
	socket.emit( 'connected', {
		data : 'User Connected',
	});


});


var form = $( 'form' ).on( 'submit', function(e) {
	e.preventDefault()
	var message = $( 'input.message' ).val()
	socket.emit('connect', {
		msg : message
	});
	$( 'input.message' ).val( ' ' ).focus()

});


socket.on('my response', function(msg){
	if (typeof msg.user !== 'undefined'){
		$('h1').remove()
		$('div.msg-wrapper').append('<div class="msgbbl"><b>' + $username +'</b>' + msg.msg + '</div>')
	}
});