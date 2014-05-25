jQuery(document).ready(function() {
    jQuery('.voters a').click(function(e) {
        var self = $(this);

        if (self.hasClass('nag')) {
            $('#nagModal').modal('show')
            jQuery.alert("Please log in or sign up to vote on quotes.");

        } else {
            var quote_id = $(this).data('id');
            var params = {};
            var vote_type = 'upvote';
            var delta = 0;
            if (self.hasClass('downvote')) {
                vote_type = 'downvote';
                delta = -1;
                if (self.hasClass('active')) {
                    params['delete'] = 1;
                    delta += 2;
                } else if (self.closest('.voters').find('.upvote.active').length > 0) {
                    self.closest('.voters').find('.upvote.active').toggleClass('active');
                    delta -= 1;
                }
            }
            if (self.hasClass('upvote')) {
                vote_type = 'upvote';
                delta = 1;
                if (self.hasClass('active')) {
                    params['delete'] = 1;
                    delta -= 2;
                } else if (self.closest('.voters').find('.downvote.active').length > 0) {
                    self.closest('.voters').find('.upvote.active').toggleClass('active');
                    delta += 1;
                }
            }

            self.toggleClass('active');
            jQuery.post('/'+vote_type+'/'+quote_id+'/', params);
            var scorespan = self.closest('.voters').find('.score-number');
            scorespan.text(parseInt(scorespan.text())+delta);
        }
        e.stopPropagation();
        return false;
    })
});
