(function() {

    $('#botpro-live-chat header').on('click', function() {
        $('#botpro-chat').slideToggle(300, 'swing');
    });

    $('#botpro-chat-close').on('click', function(e) {
        e.preventDefault();
        $('#botpro-live-chat').fadeOut(300);
    });

})();