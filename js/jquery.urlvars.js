/*
    from jquery-howto.blogspot.com
    
    The function returns an array/object with your URL parameters and their 
    values. For example, consider we have the following URL:

    http://www.example.com/?me=myValue&name2=SomeOtherValue
    
    Calling getUrlVars() function would return you the following array:

    {
        "me"    : "myValue",
        "name2" : "SomeOtherValue"
    }
    To get a value of first parameter you would do this:

    var first = getUrlVars()["me"];

    // To get the second parameter
    var second = getUrlVars()["name2"];
*/

$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});