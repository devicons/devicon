var gulp = require('gulp');
var minifyCSS = require('gulp-minify-css');
var concatCss = require('gulp-concat-css');
var plumber = require('gulp-plumber');

gulp.task('concat-css', function () {
  gulp.src(['./css/devicon.css', './css/devicon-colors.css'])
  .pipe(plumber())
  .pipe(concatCss('./css/devicon.min.css'))
  .pipe(gulp.dest('./'));
});

gulp.task('minify-css', function() {
  gulp.src('./css/devicon.min.css')
  .pipe(plumber())
  .pipe(minifyCSS())
  .pipe(gulp.dest('./css'))
});
