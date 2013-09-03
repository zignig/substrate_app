function send_action(action,id) {
$.get('/action/'+action+'/'+id, function(data) {
$('.result').html(data);
});
}

function add_tag(tag,id) {
$.get('/addtag/'+tag+'/'+id, function(data) {
$('.result').html(data);
});
}
