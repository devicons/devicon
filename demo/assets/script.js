var devicon = angular.module('devicon', []);
 
devicon.controller('IconListCtrl', function ($scope, $http) {

  $http.get('assets/devicon.json').success(function(data) {
    $scope.icons = data[0];
  });

});

devicon.filter('toArray', function () {
    'use strict';

    return function (obj) {
        if (!(obj instanceof Object)) {
            return obj;
        }

        return Object.keys(obj).map(function (key) {
            return Object.defineProperty(obj[key], '$key', {__proto__: null, value: key});
        });
    }
});