var pswpElement = document.querySelectorAll('.pswp')[0];

// build items array
var items = photos

// define options (if needed)


// Initializes and opens PhotoSwipe

// gallery.init();





for (let i = 0; i < thumbnails.length; i++) {
    img = thumbnails[i];
    var ele = document.createElement('img');
    ele.src = img
    ele.onclick = function() {
        var options = {
            // optionName: 'option value'
            // for example:
            index: i // start at first slide
        };
        var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
        gallery.init();
        gallery.goTo(i);
    }
    document.getElementById('gallery-container').appendChild(ele);
}