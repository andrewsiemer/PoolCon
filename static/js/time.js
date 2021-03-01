(function () {

  var clockElement = document.getElementById( "clock" );

  function updateClock ( clock ) {
    date = new Date()
    clock.innerHTML = date.toLocaleString('default', { weekday: 'long' }) + ', ' + date.toLocaleString('default', { month: 'long' }) + ' ' +  date.toLocaleString('default', { day: 'numeric' }) + ' ' + date.toLocaleTimeString();
  }

  setInterval(function () {
      updateClock( clockElement );
  }, 1000);

})(jQuery);