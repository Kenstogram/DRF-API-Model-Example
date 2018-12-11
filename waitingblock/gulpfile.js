/**
 * Gulp file to automate the various tasks
**/

var autoprefixer = require('gulp-autoprefixer');
var browserSync = require('browser-sync').create();
var csscomb = require('gulp-csscomb');
var cleanCss = require('gulp-clean-css');
var concat = require('gulp-concat');
var cssnano = require('gulp-cssnano');
var del = require('del');
var imagemin = require('gulp-imagemin');
var htmlPrettify = require('gulp-html-prettify');
var gulp = require('gulp');
var gulpIf = require('gulp-if');
var gulpRun = require('gulp-run');
var gulpUtil = require('gulp-util');
var npmDist = require('gulp-npm-dist');
var postcss = require('gulp-postcss');
var runSequence = require('run-sequence');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var postcss = require('gulp-postcss');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var useref = require('gulp-useref-plus');
var wait = require('gulp-wait');
var reload = browserSync.reload;

// Define paths

var paths = {
    dist: {
        base: 'waitingblock',
        img:  'core/static/img',
        libs: 'core/static/vendor'
    },
    base: {
        base: './',
        node: './node_modules'
    },
    src: {
        base: './',
        css:  'core/static/css',
        html: '**/*.html',
        img:  'core/static/img/**/*.+(png|jpg|gif|svg)',
        js:   'core/static/js/**/*.js',
        scss: 'core/static/scss/**/*.scss'
    }
}

// Compile SCSS

gulp.task('scss', function() {
  return gulp.src(paths.src.scss)
    .pipe(wait(500))
    .pipe(sass().on('error', sass.logError))
    .pipe(postcss([require('postcss-flexbugs-fixes')]))
    .pipe(autoprefixer({
        browsers: ['> 1%']
    }))
    .pipe(csscomb())
    .pipe(gulp.dest(paths.src.css))
    .pipe(browserSync.reload({
        stream: true
    }));
});

// Minify CSS

gulp.task('minify:css', function() {
  return gulp.src([
        paths.src.css + '/waitingblock.css'
    ])
    .pipe(cleanCss())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(paths.dist.base + '/css'))
});

// Minify JS

gulp.task('minify:js', function(cb) {
    return gulp.src([
            paths.src.base + '/core/static/js/argon.js'
        ])
        .pipe(uglify())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(paths.dist.base + '/js'))
});

// Live reload

gulp.task('browserSync', function() {
    browserSync.init({
        server: {
            baseDir: [paths.src.base, paths.base.base]
        },
    })
});

// Watch for changes

gulp.task('watch', ['browserSync', 'scss'], function() {
    gulp.watch(paths.src.scss, ['scss']);
    gulp.watch(paths.src.js, browserSync.reload);
    gulp.watch(paths.src.html, browserSync.reload);
});

// Clean

gulp.task('clean:dist', function() {
    return del.sync(paths.dist.base);
});

// Copy CSS

gulp.task('copy:css', function() {
    return gulp.src([
        paths.src.base + '/core/static/css/waitingblock.css'
    ])
    .pipe(gulp.dest(paths.dist.base + '/css'))
});

// Copy JS

gulp.task('copy:js', function() {
    return gulp.src([
        paths.src.base + '/core/static/js/argon.js'
    ])
    .pipe(gulp.dest(paths.dist.base + '/js'))
});

// Build

gulp.task('build', function(callback) {
    runSequence('clean:dist', 'scss', 'copy:css', 'copy:js', 'minify:js', 'minify:css',
        callback);
});

// Default

gulp.task('default', function(callback) {
    runSequence(['scss', 'browserSync', 'watch'],
        callback
    )
});

// Django

gulp.task('django', function() {
    const spawn = require('child_process').spawn;
    return spawn('python', ['waitingblock/manage.py', 'runserver'])
        .stderr.on('data', (data) => {
        console.log(`${data}`);
    });
});

// Take
gulp.task('styles', function() {
    gulp.src('./waitingblock/core/static/sass/main.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('style.css'))
        .pipe(gulp.dest('./waitingblock/core/static/css/'));
});

// Tell gulp to execute 'styles' every time a sass file changes
gulp.task('watch', function() {
    gulp.watch('./waitingblock/core/static/sass/**/*.sass', ['styles']);
});

// Compile main.sass into autoprefixed style.css
gulp.task('styles', function() {
    gulp.src('./waitingblock/core/static/sass/main.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('style.css'))
        .pipe(sourcemaps.init())
        .pipe(postcss([autoprefixer() ]))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./waitingblock/core/static/css/'));
});

// Initiate browsersync and point it at localhost:8000
gulp.task('browsersync', function() {
    browserSync.init({
        notify: true,
        proxy: "localhost:8000",
    });
});

gulp.task('watch', function() {
    gulp.watch('./waitingblock/core/static/sass/**/*.sass', ['styles']);

    // Tell browsersync to reload any time sass, css, html, python, or
    // javascript files change
    gulp.watch(['./**/*.{sass,css,html,py,js}'], reload);
});
