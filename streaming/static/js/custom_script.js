$(document).ready(function() {
  console.log("DOM is ready");
  $(".song-play-link").on( "click", function() {
    console.log( $(this).data('link') );
    $('.audio-wrapper source').attr('src', $(this).data('link'));
    $('.audio-wrapper').removeClass('d-none');
    $('.audio-wrapper audio')[0].load();
    $('.audio-wrapper audio')[0].play();
  });

  $(".song-delete-link").on( "click", function(event) {
    event.preventDefault();
    if (confirm('Are you sure you want to delete this song?')) {
        $.ajax({
            url: '/songs/'+$(this).data('record_id')+'/delete/',
            type: 'DELETE',
            success: function(response) {
                console.log('Delete request successful');
                window.location.href = '/my_songs/';
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
});
});