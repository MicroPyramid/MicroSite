
// difine variable nothing but defining pluggins which are going to used in below gulp
var gulp = require('gulp');
	minifycss = require('gulp-minify-css');
	concat = require('gulp-concat');
	jshint = require('gulp-jshint');
	gutil = require('gulp-util');
	less = require('gulp-less'); 
	path = require('path');

// assign tasks to gulp file
// 'css' task this task combine all css files to single .css file
gulp.task('css', function() {  
	gulp.src('files/*.css') //reg expr to get all .css files
	    .pipe(concat('les.css')) //use concat pluggin to combine
	    .pipe(gulp.dest('static/css')) // give path to store concatinated .css file 
});

//this task to give status of our .js files
gulp.task('default', function() {
  gulp.src('files/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter('default'));

   
});

//task to convert .less file to .css file
gulp.task('csss', function () {  
  return gulp.src('files/*.less')
    .pipe(less({
      paths: [ path.join(__dirname, 'less', 'includes') ]
    })) //funtion to compile .less file
    .pipe(gulp.dest('static/css'))
    .on('error', gutil.log);
});

// function to combine all javascript files to single .js file
gulp.task('script', function(){
	return gulp.src('files/*.js')
	.pipe(concat('javascriptfile.js'))
	.pipe(gulp.dest('static/js'))
});


