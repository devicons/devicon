var gulp      = require('gulp');
var minifyCSS = require('gulp-minify-css');
var concatCss = require('gulp-concat-css');
var plumber   = require('gulp-plumber');


function concat() {
    return gulp.src(['./devicon.css', './devicon-alias.css', './devicon-colors.css'])
        .pipe(plumber())
        .pipe(concatCss('./devicon.min.css'))
        .pipe(gulp.dest('./'));
}

function minify() {
    return gulp.src('./devicon.min.css')
        .pipe(plumber())
        .pipe(minifyCSS())
        .pipe(gulp.dest('./'))
}

exports.concat = concat;
exports.minify = minify;
exports.default = gulp.series(concat, minify);