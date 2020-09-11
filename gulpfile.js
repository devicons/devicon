var gulp      = require('gulp');
var minifyCSS = require('gulp-minify-css');
var concatCss = require('gulp-concat-css');
var plumber   = require('gulp-plumber');
const fsPromise = require('fs/promises');
const path = require("path");

/**
 * Create the CSS files from the devicon.json.
 */
async function createCSSFiles() {
    const deviconJson = JSON.parse(
        await fsPromise.readFile(
            path.join(__dirname, "devicon.json"), "utf8"
        )
    );

    createAliasCSS(deviconJson);
    createColorsCSS(deviconJson);
}

/**
 * Create an alias css file in the root dir based on the devicon.json  
 * @param {Object} deviconJson, the object read from the
 * devicon.json file. 
 */
async function createAliasCSS(deviconJson) {
    let css = await fsPromise.readFile(
        path.join(__dirname, "devicon.css"), "utf8"
    );

    let statements = css.match(/\.devicon-(.*\s+){2,}?(?=})/g).map(str => 
		createAliasesStatement(str, deviconJson));
}


/**
 * Create the aliases statement by searching for the 
 * techname in the statement and finding its aliases in
 * the deviconJson.
 * @param {String} str, a css selector str 
 * @param {Object} deviconJson, an object that maps the
 * technology name to the content string.
 */
function createAliasesStatement(str, deviconJson) {
    try {
        const TECH_NAME_REG_EXP = /(?<=-)(\w+-)*(?=-)/ig;
        let techName = str.match(TECH_NAME_REG_EXP)[0];
    } catch(e) {
        console.log(str);
        console.error(e);
    }
}

/**
 * Create a colors css file in the root dir based on the deviconJson.
 * @param {Object} deviconJson, the object read from the
 * devicon.json file. 
 */
function createColorsCSS(deviconJson) {
    // create the color statements for each font object
    let statements = deviconJson.map(fontObj => {
        let {
            name, 
            versions: {
                font: fonts
            },
            color
        } = fontObj;

        // loop through the fonts and create css classes
        let cssClasses = fonts.map(font => `.devicon-${name}-${font}`);
        // make the statement
        return `${cssClasses.join(",")}{color: ${color}}`;
    });

    let cssPath = path.join(__dirname, "devicon-colors.css");
    fsPromise.writeFile(cssPath, statements, (err) => {
        if (err) console.log(err);
    })
}

/**
 * Concat the devicon.css, the devicon-aias.css and the
 * devicon-colors.css together. Pipe the result into
 * the devicon.min.css.
 */
function concat() {
    return gulp.src(['./devicon.css', './devicon-alias.css', './devicon-colors.css'])
        .pipe(plumber())
        .pipe(concatCss('./devicon.min.css'))
        .pipe(gulp.dest('./'));
}

/**
 * Minify the devicon.min.css file.
 */
function minify() {
    return gulp.src('./devicon.min.css')
        .pipe(plumber())
        .pipe(minifyCSS())
        .pipe(gulp.dest('./'))
}

exports.concat = concat;
exports.minify = minify;
exports.test = test;
exports.default = gulp.series(concat, minify);