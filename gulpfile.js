var gulp      = require('gulp');
const sass = require('gulp-sass');
sass.compiler = require('sass')
const fsPromise = require('fs').promises;
const path = require("path");

// global const
const deviconJSONName = "devicon.json";
const aliasSCSSName = "devicon-alias.scss";
const colorsCSSName = "devicon-colors.css";
const finalMinSCSSName = "devicon.min.scss";


/**
 * Create the devicon.min.css by creating needed
 * css files and compiling them together using Sass.
 */
async function createDeviconMinCSS() {
    await createCSSFiles();

    let deviconMinPath = path.join(__dirname, finalMinSCSSName);
    // recall that devicon-alias.scss imported the devicon.css => don't need
    // to reimport that file.
    const fileContent = `@use "${aliasSCSSName}";@use "${colorsCSSName}";`;
    await fsPromise.writeFile(deviconMinPath, fileContent, "utf8");

    return gulp.src(finalMinSCSSName)
        .pipe(sass.sync({"outputStyle": "compressed"}).on('error', sass.logError))
        .pipe(gulp.dest('./'));
}

/**
 * Create the devicon-alias.scss and the
 * devicon-colors.css from the devicon.json.
 */
async function createCSSFiles() {
    const deviconJson = JSON.parse(
        await fsPromise.readFile(
            path.join(__dirname, deviconJSONName), "utf8"
        )
    );

    await Promise.all([
        createAliasSCSS(deviconJson),
        createColorsCSS(deviconJson)
    ])
}

/**
 * Create an alias scss file in the root dir based on the devicon.json.
 * This function will use sass instead of normal css.
 * This is due to sass's ability to extend classes => Make it easier
 * to create aliases classes.
 * @param {Object} deviconJson, the object read from the
 * devicon.json file. 
 * @return a Promise that'll resolve when the devicon-alias.scss is
 * created.
 */
function createAliasSCSS(deviconJson) {
    let statements = deviconJson.map(createAliasStatement).join(" ");
    let sass = `@use "devicon";${statements}`;
    let sassPath = path.join(__dirname, aliasSCSSName);
    return fsPromise.writeFile(sassPath, sass, "utf8");
}


/**
 * Create the aliases statement by searching for the 
 * techname in the statement and finding its aliases in
 * the deviconJson.
 * @param {Object} fontObj, a devicon font object.
 * @return a string representing a css statement of the
 * devicon-alias.scss.
 */
function createAliasStatement(fontObj) {
    let {
        name,
        aliases
    } = fontObj;

    return aliases.map(aliasObj => {
        return `.devicon-${name}-${aliasObj.alias} {
            @extend .devicon-${name}-${aliasObj.base};
        }`;
    }).join(" ");
}

/**
 * Create a colors css file in the root dir based on the deviconJson.
 * @param {Object} deviconJson, the object read from the
 * devicon.json file. 
 * @return a Promise that'll resolve when the devicon-alias.scss is
 * created.
 */
function createColorsCSS(deviconJson) {
    // create the color statements for each font object
    let statements = deviconJson.map(fontObj => {
        let {
            name, 
            versions: {
                font: fonts
            },
            color,
            aliases
        } = fontObj;

        if (fonts.length === 0 || typeof(color) !== "string") {
            console.log(`This object doesn't have a font or a color: ${name}`);
            return "";
        } 

        // process the icons in the font attr
        let cssClasses = fonts.map(font => `.devicon-${name}-${font}.colored`);

        // process the icons in the aliases attr
        aliases.forEach(aliasObj => {
            cssClasses.push(`.devicon-${name}-${aliasObj["alias"]}.colored`);
        });

        return `${cssClasses.join(",")}{color: ${color}}`;
    }).join(" ");

    let cssPath = path.join(__dirname, colorsCSSName);
    return fsPromise.writeFile(cssPath, statements, "utf8");
}

/**
 * Remove the devicon-alias.scss, devicon-colors.css, 
 * and the devicon.min.scss.
 */
function cleanUp() {
    let fileNames = [
        aliasSCSSName,
        colorsCSSName,
        finalMinSCSSName,
    ];

    return Promise.all(
        fileNames.map(name => {
            try {
                let filePath = path.join(__dirname, name);
                return fsPromise.unlink(filePath);
            } catch(e) {
                console.log(e);
            }
        })
    );
}


exports.updateCss = createDeviconMinCSS;
exports.clean = cleanUp;
