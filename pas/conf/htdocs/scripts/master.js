Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};

Array.prototype.removeEl = function (value) {
    return this.remove(this.indexOf(value));
}

var updateConversationLabel = function () {
    var all = $('.conversation-filter input').size(),
        selected = $('.conversation-filter input:checked').size(),
        text;
    
    if (all == selected) {
        text = "All conversations";
    } else if (selected > 1) {
        text = selected + " conversations";
    } else if (selected == 1) {
        text = "1 conversation";
    } else {
        text = "No conversations";
    }
    
    $('.conversation-filter button').text(text);
};

var filter = function (level) {
    switch (level) {
        case 3:
            $('.transactions').addClass('push-only');
        case 2:
            $('.syn2, .syn1, .fin1, .fin2').addClass('smart');
        case 1:
            $('.transactions').addClass('no-ack');
    }
    
    $('.conversation-filter input:not(:checked)').each(function () {
        $("." + $(this).val()).addClass('hidden');
    });
};

var unfilter = function (level) {
    $('.conversation-filter input:checked').each(function () {
        $("." + $(this).val()).removeClass('hidden');
    });
    
    switch (level) {
        case 0:
            $('.transactions').removeClass('no-ack');
        case 1:
            $('.syn2, .syn1, .fin1, .fin2').removeClass('smart');
        case 2:
            $('.transactions').removeClass('push-only');
    }
};

var applyFilters = function (level) {
    level |= $('.frame-filter-bar li.active').index();
    
    unfilter(level);
    filter(level);
};

var updatePorts = function () {
    var $tr = $('.transactions'),
        pos = [];
    
    $('.port.hover', $tr).removeClass('hover');
    
    $($tr.data('active')).each(function (el) {
        $('.port:nth-child(' + (this + 2) + ')').addClass('hover');
        pos.push(this * 26 + 56 + "px");
        pos.push(this * 26 + 56 + "px");
    });
    
    $($tr.data('sticky')).each(function (el) {
        $('.port:nth-child(' + (this + 2) + ')').addClass('hover');
        pos.push(this * 26 + 56 + "px");
        pos.push(this * 26 + 56 + "px");
    });
    
    $tr.css('background-position-x', pos.join(', '));
};

$(function () {
    $('nav ul li a').click(function (e) {
        $(this).closest('ol, ul').find('li').removeClass('active');
        $(this).closest('li').addClass('active');
    });
    
    $('body > section').spawnHeight(window, $('body > nav'));
    
    $('.flags-filter a').click(function (e) {
        e.preventDefault();
        applyFilters($(this).parent().index());
    });
    
    $('.details-switch a').click(function (e) {
        e.preventDefault();
        
        $li = $(this).parent();
        
        switch ($li.index()) {
            case 0:
                $('.transactions tr.details').removeClass('details');
                break;
            case 1:
                $('.transactions tr:not(.no-payload)').addClass('details');
                break;
        }
    });
    
    $('.bindstatus-filter a').click(function (e) {
        e.preventDefault();
        
        var level = $(this).parent().index();
        
        switch (level) {
            case 0:
                $('.bindstatus-request, .bindstatus-response').removeClass('smart');
            case 1:
                $('.bindstatus-request, .bindstatus-response').removeClass('bindstatus-hidden');
        }
        
        switch (level) {
            case 2:
                $('.bindstatus-request, .bindstatus-response').addClass('bindstatus-hidden');
            case 1:
                $('.bindstatus-request, .bindstatus-response').addClass('smart');
        }
        
    });
    
    $('.conversation-filter button').click(function (e) {
        var c = $('.conversation-filter > div');
        
        if (!c.hasClass('open')) {
            // Otherwise the event propagation would fire the body callback
            // straight away
            e.stopPropagation();
            
            c.addClass('open');
            
            $('body').one('click', function () {
                c.removeClass('open');
            });
        } else {
            c.removeClass('open');
        }
    });
    
    $('.conversation-filter ol').click(function(e){
        e.stopPropagation();
    });
    
    $('.frame-filter-bar li:not(.active) a').lockDimensions('width');
    $('.frame-filter-bar .active').removeClass('active')
        .find('a').lockDimensions('width')
        .closest('li').addClass('active');
    
    $('.conversation-filter input').change(function () {
        applyFilters();
        updateConversationLabel();
    });
    
    $('.transactions').data('active', []);
    $('.transactions').data('sticky', []);
    
    $('.transactions tbody tr:not(:first-child)').hover(function () {
        var from = $('td.before', this).attr('colspan'),
            span = $('td.transaction', this).attr('colspan');
        
        if (from === undefined) {
            from = 0;
        }
        
        $('.transactions').data('active', [from, from + span - 1]);
        
        updatePorts();
    }, function () {
        $('.transactions').data('active', []);
        updatePorts();
    }).click(function () {
        if (!$(this).hasClass('no-payload')) {
            $(this).toggleClass('details');
            
            var s = $('.transactions tbody tr.details').size();
            
            $('.details-switch li.active').removeClass('active');
            
            if (s == 0) {
                $('.details-switch li:nth-child(1)').addClass('active');
            } else if (s == $('.transactions tbody tr:not(.no-payload)').size()) {
                $('.details-switch li:nth-child(2)').addClass('active');
            }
        }
    });
    
    $('.transactions tbody td:last-child .details').click(function (e) {
        e.stopPropagation();
    })
    
    $('.transactions th.port').hover(function () {
        $('.transactions').data('active', [$(this).index()-1]);
        updatePorts();
    }, function () {
        $('.transactions').data('active', []);
        updatePorts();
    }).click(function () {
        var $this = $(this),
            $tr = $('.transactions');
        
        if ($this.hasClass('active')) {
            $this.removeClass('active');
            $tr.data('sticky').removeEl($this.index() - 1);
        } else {
            $this.addClass('active');
            $tr.data('sticky').push($this.index() - 1);
        }
        
        updatePorts();
    });
});










