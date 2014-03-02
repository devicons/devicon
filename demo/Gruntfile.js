'use strict';

/*
| _________________________________________________
|
|   Livereload and connect variables
| _________________________________________________
|
*/
var LIVERELOAD_PORT = 35729;
var lrSnippet = require('connect-livereload')({
  port: LIVERELOAD_PORT
});
var mountFolder = function (connect, dir) {
  return connect.static(require('path').resolve(dir));
};

/*
| _________________________________________________
|
|   Grunt module
| _________________________________________________
|
*/
module.exports = function(grunt) {

  /*
  |   Dynamically load npm tasks
  | _________________________________________________
  |
  */
  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

  /*
  |   Project configuration
  | _________________________________________________
  |
  */
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    /*
    |   Connect port/livereload
    | _________________________________________________
    |
    */
    connect: {
      options: {
        port: 9000,
        hostname: '*'
      },
      livereload: {
        options: {
          middleware: function (connect) {
            return [lrSnippet, mountFolder(connect, '.')];
          }
        }
      }
    },

    /*
    | _________________________________________________
    |
    |   Copy task
    | _________________________________________________
    |
    */
    copy: {
      dev: {
        files: [
          {
            src:'../font/*', 
            dest:'assets/font',
            flatten:true, 
            filter:'isFile', 
            expand:true 
          },
          {
            src:'../scss/devicon.scss', 
            dest:'assets/scss/', 
            flatten:true, 
            filter:'isFile', 
            expand:true 
          }
        ],
      },
    },

    /*
    |   Build bower components
    | _________________________________________________
    |
    */
    bower: {
      dev: {
        dest: 'assets/components/'
      },
      dist: {
        dest: 'assets/components/'
      }
    },

    /*
    |   Opens the web server in the browser
    | _________________________________________________
    |
    */
    open: {
      server: {
        path: 'http://localhost:<%= connect.options.port %>'
      }
    },

    /*
    | _________________________________________________
    |
    |   Sass task
    | _________________________________________________
    |
    */
    sass: {
      dev: {
        options: {
          style: 'expanded',
          compass: true
        },
        files: {
          'assets/style.css': 'assets/scss/style.scss'
        }
      },
      prod: {
        options: {
          style: 'compressed',
          compass: true        
        },
        files: {
          'assets/style.css': 'assets/scss/style.scss'
        }
      },
    },

    /*
    | _________________________________________________
    |
    |   Watch task
    | _________________________________________________
    |
    */
    watch: {
      sass: {
        files: 'assets/scss/**/*.scss',
        tasks: ['sass:dev']
      },
      copy: {
        files: [
          '../font/*',
          '../scss/devicon.scss'
        ],
        tasks: ['copy:dev']
      },
      livereload: {
        options: {
          livereload: LIVERELOAD_PORT
        },
        files: [
          'assets/**/*.css',
          'assets/**/*.js',
          '**/*.html'
        ]
      }
    }

  });

  /*
  | _________________________________________________
  |
  |   Register task
  | _________________________________________________
  |
  */
  grunt.registerTask('default', ['copy:dev','bower:dev','sass:dev','connect:livereload','open','watch']);
  grunt.registerTask('prod', ['sass:prod']);

};