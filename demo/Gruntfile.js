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
    |   Project variables
    | _________________________________________________
    |
    */
    project: {

      src_bower: '<%= project.src %>/bower_components',
      src_components: '<%= project.src %>/components',
      src_scss: '<%= project.src %>/scss',
      src_js: '<%= project.src %>/js',

    },

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
    |   Copy task
    | _________________________________________________
    |
    */
    copy: {
      dev: {
        files: [
          {src:'<%= project.src_components %>/**/*.blade.php', dest:'<%= project.dist_views %>/layouts/components/', flatten:true, filter:'isFile', expand:true }
        ],
      },
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
          compass: true,
          loadPath: '<%= project.src_bower %>/foundation/scss'
        },
        files: {
          '<%= project.dist_css %>/main.min.css': '<%= project.src_scss %>/main.scss'
        }
      },
      prod: {
        options: {
          style: 'compressed',
          compass: true,
          loadPath: '<%= project.src_bower %>/foundation/scss'
        },
        files: {
          '<%= project.dist_css %>/main.min.css': '<%= project.src_scss %>/main.scss'
        }
      },
    },

    /*
    | _________________________________________________
    |
    |   Concat task
    | _________________________________________________
    |
    */
    concat: {
      dev: {
        files: {

          /* Create page.js
          ----------------- */
          /*'<%= project.dist_js %>/page.min.js': [
            '<%= project.src_components %>/component/component.js',
            '<%= project.src_js %>/page.js',
          ],*/
        }
      }
    },

    /*
    | _________________________________________________
    |
    |   Uglify task
    | _________________________________________________
    |
    */
    uglify: {
      dev: {
        files: {
          '<%= project.dist_js %>/modernizr.min.js': '<%= project.src_bower %>/modernizr/modernizr.js'
        }
      },
      prod: {
        files: {
          '<%= project.dist_js %>/modernizr.min.js': '<%= project.src_bower %>/modernizr/modernizr.js'
          /* Create page.js
          ----------------- */
          /*'<%= project.dist_js %>/page.min.js': [
            '<%= project.src_components %>/component/component.js',
            '<%= project.src_js %>/page.js',
          ],*/
        }
      }
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
      uglify: {
        files: 'assets/js/**/*.js',
        tasks: ['concat:dev']
      },
      livereload: {
        options: {
          livereload: LIVERELOAD_PORT
        },
        files: [
          'assets/**/*.css',
          'assets/**/*.js'
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
  grunt.registerTask('default', ['sass:dev','bower:dev','concat:dev','connect:livereload','open','watch']);
  grunt.registerTask('prod', ['copy:dev','sass:prod','uglify:prod']);

};