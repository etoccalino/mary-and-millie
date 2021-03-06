// Namespace for the application.
var Requests = {

  // --- Constants for the DOM ---

  // Map the "status" of a request to a selector for the corresponding table.
  tables: {
    NEW: '#new-requests',
    PENDING: '#pending-requests',
    DONE: '#done-requests'
  },

  // --- Utility functions ---

  // Create a new row for a requests table, using data comming from the server.
  createRequestRow: function (requestData) {
    console.log('createRequestRow() called. with requestData: ' + requestData);
    var obj = JSON.parse(requestData)
      , row = '';

    row += '<tr><td><div>' + '(who?)' + '</div></td>';
    row += '<td><div><a href="' + obj.meta.url + '">' + obj.meta.description + '</a></div></td>';
    row += '<td><div><time class="timeago" datetime="' + obj.request_time + '"></time></div></td></tr>';

    console.log('new row text is: ' + row);
    return $(row)
  },

  // Insert a request row (a jQuery object) into a particular request table (identified by ID).
  insertRequestRow: function (requestRow, requestTableID) {
    console.log('inserting before "' + requestTableID + ' tr:first".');
    var contents = $('div', requestRow);
    contents.css('display', 'none');
    $('.timeago', contents).timeago();
    $(requestTableID + ' tr:first').before(requestRow);
    contents.fadeIn('fast');
  },

  // --- Socket to handle requests events ---

  socket: io.connect('/requests'),

};

// Bind the events desired.
Requests.socket.on('connect', function () {

  console.log('connected to the "/requests" namespace.')

  // Complete a 3-way handshake to force the initialization of the namespace.
  Requests.socket.emit('new client');

  Requests.socket.on('new request', function (requestData) {
    var row = Requests.createRequestRow(requestData);
    Requests.insertRequestRow(row, Requests.tables.NEW);
  });

});
