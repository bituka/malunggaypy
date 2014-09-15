/**
* Created with pelikula.
* User: stoned-code-warrior
* Date: 2014-06-24
* Time: 10:23 PM
* To change this template use Tools | Templates.
*/
$(function () {
//	alert('test');
	$('div.pelikula-entries:nth-child(4n)').after('</div><div class="row">');
});
$(document).ready(function() {
//	alert('test');
});

$(function () {
    /*
    $.ajax({
        url: "/searchentries",
    }).done(function (data) {
        $('#searchentries').autocomplete({
            source: data,
            minLength: 2
        });
    });
    */

    
	$('#searchentries').autocomplete({
        source: "/searchentries",
    // 	source:[ "ass ddd", "Choice2", "bbbtestsss", "tae MO Pau" ],
        minLength: 2,
        select: function( event, ui ) {
        log( ui.item ?
          "Selected: " + ui.item.value + " aka " + ui.item.id :
          "Nothing selected, input was " + this.value );
      }
      
      /*
        select: function(event, ui) {
            var url = ui.item.id;
            if(url != '#') {
                location.href = '/searchentries/' + url;
            }
        },
        */
    //    html: true, // optional (jquery.ui.autocomplete.html.js required)
 
      // optional (if other layers overlap autocomplete list)
    //    open: function(event, ui) {
    //        $(".ui-autocomplete").css("z-index", 1000);
    //    }
    });

});
