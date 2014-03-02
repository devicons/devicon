var phonecatApp = angular.module('devicon', []);
 
phonecatApp.controller('IconListCtrl', function ($scope, $http) {
  $http.get('assets/devicon.json').success(function(data) {
    $scope.icons = data[0];
  });
 
});