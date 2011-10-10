var getInfoLink = function(name){
        return 'http://wikitravel.org/en/'+name;
    }
    
var getFlightsLink = function(name){
        return 'http://skyscanner.net/as/ashx?t='+name;
    }

var addToResults = function(place){
    var $place = $('<div/>',{
        class:'place',
        name:place.name,
        html:'<h3>'+place.name+'</h3>'
    });
    
    var $info = $('<p>'+place.info+'</p>');
    $('<a/>',{
        html:' ...',
        href:getInfoLink(place.name),
        target:'_blank'
    }).appendTo($info);
    $info.appendTo($place);
    
    $('<a/>',{
        html:'Get Me There!',
        href:getFlightsLink(place.name),
        target:'_blank'
    }).appendTo($place);
    $('#responseContainer').append($place);
};

var InfoRequest = {
    makeRequest:function(placeName){
        $.ajax({
            url:'/services/info/'+placeName,
            type:'GET',
            dataType:'json',
            success:this.succeed,
            error:this.failed
        });
    },
    succeed:function(response){
        addToResults(response);
        console.log('Success!');
    },
    failed:function(response){
        console.error('Could not get result');
    }
};

var SearchRequest = {
    makeRequest:function(searchTerm){
        $.ajax({
            url:'/services/suggest/'+searchTerm,
            type:'GET',
            dataType:'json',
            success:this.succeed,
            error:this.failed
        });
    },
    succeed:function(response){
        for(i in response[0]){
            InfoRequest.makeRequest(response[0][i]);
        }
        console.log('Success!');
    },
    failed:function(response){
        console.error('Could not get result');
    }
};

$(document).ready(function(){
    $('#searchButton').click(function(){
        SearchRequest.makeRequest($('#searchbox').val());
    });
    $('#searchbox').keyup(function(event){
        if(event.keyCode==13){
            $('#searchButton').click();
        }
    });
});