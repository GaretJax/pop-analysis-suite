(function ($) {
    $.fn.spawnHeight = function (parent) {
        
        var elements = this,
            $parent = $(parent),
            _blocks = [],
            $blocks,
            height,
            _onResize;
        
        for (var i = 1; i<arguments.length; i++) {
            _blocks[i-1] = $(arguments[i]);
        }
        
        $blocks = $(_blocks);
        
        _onResize = function () {
            height = $blocks.sumHeight()
            
            elements.each(function () {
                $(this).height($parent.height() - height);
            });
        };
        
        $(window).resize(_onResize);
        
        _onResize();
    };
    
    $.fn.lockDimensions = function (type) {  
        return this.each(function() {
            var $this = $(this);

            if ( !type || type == 'width' ) {
                $this.width( $this.width() );
            }

            if ( !type || type == 'height' ) {
                $this.height( $this.height() );
            }

        });
    };
    
    $.fn.sumHeight = function () {
        var sum = 0;
        
        this.each(function () {
            sum += $(this).outerHeight(true);
        });
        
        return sum;
    };
})(jQuery);