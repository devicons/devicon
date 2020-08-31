const path = require("path");
const fs = require("fs");

/**
 * Parse through the input.json and get all the 
 * svg files within the new folder(s) as listed.
 * @param {{
 * 	folderName: string, 
 * 	"originalSameAsPlain": boolean,
	"color": string
	}[]} input, an array of icon objects
 */
async function parseInput(input) {
  let svgFontFilePaths = [];
  let colors = [];

  input.forEach(async iconObj => {
    let {folderName, originalSameAsPlain, color} = iconObj;
	colors.push(color);

	// if original is same as plain (aka true), we use
	// the original version. else, we use plain.
    let allowedFontVers = [
      parseInt(originalSameAsPlain) ? "original" : "plain",
      "line",
    ];

	await getFolderFontFiles(folderName, allowedFontVers, svgFontFilePaths)
  })

  return {
    svgFontFilePaths,
    colors
  };
}


/**
 * Get the eligible SVG files from the folder.
 * @param {String} folderName, the name of the folder
 * @param {String[]} allowedFontVers, an array of allowed
 * font version. This makes sure that we only add the 
 * appropriate files to the svgFilePaths.
 * @param {String[]} svgFilePaths, an array of filepaths
 * to eligible svg files that can be used as fonts.
 */
async function getFolderFontFiles(folderName, allowedFontVers, svgFilePaths) {
	// the new folder(s) must be in the icons folder
    let folderPath = path.join(__dirname, "icons", folderName);
    let dir = await new Promise((resolve, reject) => {
      fs.opendir(folderPath, (err, dir) => {
        if (err) reject(err);
        else resolve(dir);
      });
    });


    let dirEntry;
    while (dirEntry = await dir.read()) {
      // check if it's an SVG file
      let entryName = dirEntry.name;
      if (dirEntry.isFile() && entryName.match(/\.svg$/)) {
        // check if it has the correct type to use as a font
        if (allowedFontVers.some(allowedVer =>
            entryName.match(new RegExp(allowedVer)))) {

          svgFilePaths.push(path.join(folderPath, dirEntry.name));
        }
      }
    }
}


module.exports = parseInput;