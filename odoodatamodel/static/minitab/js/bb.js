//odoo.define('mini_tableau.bb', function (require) {
//  "use strict";
//
//  var core = require('web.core');
//  var rpc = require('web.rpc');
//
//  var savedQueries = [];
//
//  function saveQuery() {
//    var inputQuery = document.getElementById('input-query');
//    var query = inputQuery.value;
//    var name = prompt("Enter a name for your query:");
//
//    // Create a new record in the Odoo backend
//    rpc.query({
//      model: 'mini.tableau',
//      method: 'create',
//      args: [{
//        name: name,
//        query: query
//      }]
//    }).then(function(result) {
//      // Record created successfully
//      inputQuery.value = '';
//      updateSavedQueries();
//    }).catch(function(error) {
//      // Error occurred while creating the record
//      console.error(error);
//    });
//  }
//
//  function deleteQuery(id) {
//    // Delete the record from the Odoo backend
//    rpc.query({
//      model: 'mini.tableau',
//      method: 'unlink',
//      args: [[id]]
//    }).then(function(result) {
//      // Record deleted successfully
//      updateSavedQueries();
//    }).catch(function(error) {
//      // Error occurred while deleting the record
//      console.error(error);
//    });
//  }
//
//  function updateSavedQueries() {
//    var savedQueriesDiv = document.getElementById('saved-queries');
//    savedQueriesDiv.innerHTML = '';
//
//    // Retrieve the saved queries from the Odoo backend
//    rpc.query({
//      model: 'mini.tableau',
//      method: 'search_read',
//      domain: [],
//      fields: ['name']
//    }).then(function(result) {
//      // Display the saved queries
//      result.forEach(function(record) {
//        var queryName = record.name;
//        var queryElement = document.createElement('div');
//        queryElement.textContent = queryName;
//
//        var deleteButton = document.createElement('button');
//        deleteButton.textContent = 'Delete';
//        deleteButton.addEventListener('click', function() {
//          deleteQuery(record.id);
//        });
//
//        queryElement.appendChild(deleteButton);
//        savedQueriesDiv.appendChild(queryElement);
//      });
//    }).catch(function(error) {
//      // Error occurred while retrieving the saved queries
//      console.error(error);
//    });
//  }
//
//  function populateInput(queryName) {
//    // Retrieve the query from the Odoo backend
//    rpc.query({
//      model: 'mini.tableau',
//      method: 'search_read',
//      domain: [['name', '=', queryName]],
//      fields: ['query']
//    }).then(function(result) {
//      if (result.length > 0) {
//        var inputQuery = document.getElementById('input-query');
//        inputQuery.value = result[0].query;
//      }
//    }).catch(function(error) {
//      // Error occurred while retrieving the query
//      console.error(error);
//    });
//  }
//
//  updateSavedQueries();
//
//});
