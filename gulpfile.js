var gulp = require('gulp');
var minifyCSS = require('gulp-minify-css');
var concatCss = require('gulp-concat-css');
var less = require('gulp-less');
var plumber = require('gulp-plumber');
var path = require('path');

gulp.task('concat-css', function () {
  gulp.src(['./devicon.css', './devicon-colors.css'])
  .pipe(plumber())
  .pipe(concatCss('./devicon.min.css'))
  .pipe(gulp.dest('./'));
});

gulp.task('minify-css', function() {
  gulp.src('./devicon.min.css')
  .pipe(plumber())
  .pipe(minifyCSS())
  .pipe(gulp.dest('./'))
});

gulp.task('less', function () {
  return gulp.src('./less/devicon.less')
      .pipe(less({
        paths: [ path.join(__dirname, 'less', 'includes') ]
      }))
      .pipe(gulp.dest('./'));
});