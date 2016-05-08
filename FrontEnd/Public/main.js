var map;
    $( "#startButton" ).click(function() {
      alert( "Handler for .click() called." );
      console.log("Button was clicked");
    });

    $( document ).ready(function() {
        console.log( "ready!" );
        initialize();
    });

    function initialize() {
      callOtherDomain();
      var mapOptions = {
        center: new google.maps.LatLng(36.1699,115.1398),
        //center: new google.maps.LatLng(51.503454,-0.119562),
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };

      map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

      // geolocation function call goes here

      var infoWindow = new google.maps.InfoWindow({map: map});

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }

      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
      }

      // geolocation function ends here
      
    }

    // $.getJSON( "https://helping-hand-sadrusaleem.c9users.io/", {}).done(function( data ) {
    //   $.each( data.items, function( i, item ) {
    //     console.log(i,item)
    //   });
    // });

    //CROSS SITE XHR

  var isIE8 = window.XDomainRequest ? true : false;
  var invocation = createCrossDomainRequest();
  var url = 'https://helping-hand-sadrusaleem.c9users.io/';
  var jsonData;

  function createCrossDomainRequest(url, handler) {
    var request;
    if (isIE8) {
      request = new window.XDomainRequest();
      }
      else {
        request = new XMLHttpRequest();
      }
    return request;
  }

  function callOtherDomain() {
    if (invocation) {
      if(isIE8) {
        invocation.onload = outputResult;
        invocation.open("GET", url, true);
        invocation.send();
        invocation.onload = function () {
        var jsonData = $.parseJSON(invocation.responseText);
        // other code goes here
        setMarkers
        };
      }
      else {
        invocation.open('GET', url, true);
        invocation.onreadystatechange = handler;
        invocation.send();
        // jsonData = invocation.responseText;
        // setMarkers(map);
        invocation.onload = function () {
        var jsonData = $.parseJSON(invocation.responseText);
        // other code goes here
        setMarkers
        };
      }
    }
    else {
      var text = "No Invocation TookPlace At All";
      var textNode = document.createTextNode(text);
      var textDiv = document.getElementById("textDiv");
      textDiv.appendChild(textNode);
    }
  }

  function handler(evtXHR) {
    if (invocation.readyState == 4)
    {
      if (invocation.status == 200) {
          outputResult();
      }
      else {
        alert("Invocation Errors Occured");
      }
    }
  }

  function outputResult() {
    var response = invocation.responseText;
    // var textDiv = document.getElementById("textDiv");
    // textDiv.innerHTML += response;
    jsonData = response;
    setMarkers(map);
  }

  function createInfo(arr,marker){
    var contentString ='<div id="content"><h1>' + arr[0] + '</h1><p><b>Address: </b>' + arr[5] + '</p><p><b>Phone Number: </b>' + arr[7] + '</p></div>';

    var infowindow = new google.maps.InfoWindow({
        content: contentString
      });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
      });
  }

    // CROSS SITE XHR ends here


    // var beaches = [
    //   ['Bondi Beach', -33.890542, 151.274856, 4],
    //   ['Coogee Beach', -33.923036, 151.259052, 5],
    //   ['Cronulla Beach', -34.028249, 151.157507, 3],
    //   ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
    //   ['Maroubra Beach', -33.950198, 151.259302, 1]
    // ];

    var locations = [];
     // MARKER IMAGES
     // http://lalude.com/adesina/HelpingHandSupport/iconBurger1.png

    function setMarkers(map) {
      //Get the data from the json object

      jsonData = JSON.parse(jsonData);

      //console.log(obj);
      for(i in jsonData.data){
        console.log(jsonData.data[i]);
        locations.push([jsonData.data[i].name,
                        jsonData.data[i].lat,
                        jsonData.data[i].long,
                        jsonData.data[i].service_type,
                        parseInt(i)+1,
                        jsonData.data[i].address,
                        jsonData.data[i].status,
                        jsonData.data[i].phone]);
      }
      console.log(locations)

      // Adds markers to the map.

      // Marker sizes are expressed as a Size of X,Y where the origin of the image
      // (0,0) is located in the top left of the image.

      // Origins, anchor positions and coordinates of the marker increase in the X
      // direction to the right and in the Y direction down.
      var bed = {
        url: 'http://lalude.com/adesina/HelpingHandSupport/iconBed1.png',
        size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
      };
      var bedGreen = {
        url: 'http://lalude.com/adesina/HelpingHandSupport/iconBedOpen.png',
        size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
      };
      var food = {
        url: 'http://lalude.com/adesina/HelpingHandSupport/iconFood1.png',
        size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
      }
      var foodGreen = {
        url: 'http://lalude.com/adesina/HelpingHandSupport/iconFoodOpen.png',
        size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
      }
      var cross = {   
        url: 'http://lalude.com/adesina/HelpingHandSupport/iconDoctor1.png',
        size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
      }
      var crossGreen = {   
        url: 'http://lalude.com/adesina/HelpingHandSupport/iconDoctorOpen.png',
        size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
      }
      var shape = {
        coords: [1, 1, 1, 20, 18, 20, 18, 1],
        type: 'poly'
      };
      var infoArr = [];
      for (var i = 0; i < locations.length; i++) {
        var imageType;
        var location = locations[i];
        if(location[3] == 1){
          if(location[6] == 1){
            imageType = bedGreen;
          } else{
          imageType = bed;
          }
        } else if(location[3] == 2){
          if(location[6] == 1){
            imageType = foodGreen;
          } else{
          imageType = food;
          }
        } else if(location[3] == 3){
          if(location[6] == 1){
            imageType = crossGreen;
          } else{
          imageType = cross;
          }
        }


        var marker = new google.maps.Marker({
          position: {lat: location[1], lng: location[2]},
          map: map,
          icon: imageType,
          shape: shape,
          title: location[0],
          zIndex: location[4]
        });

        createInfo(location,marker);
      }
    }