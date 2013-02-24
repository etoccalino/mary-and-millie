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
    console.log('createRequestRow() called.');
  },

  // Insert a request row into a particular request table (identified by the mapping).
  insertRequestRow: function (requestRow, requestTable) {
    console.log('insertRequestRow() called.');
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
