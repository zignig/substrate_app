function send_action(action,id) {
$.get('/action/'+action+'/'+id, function(data) {
$('.result').html(data);
});
}
