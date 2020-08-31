/* Parse the devicon-colors.css and convert it to devicon-colors.json*/
const fs = require("fs");
const path = require('path');

function main() {
	let colorsMap = constructColorsMap();
	createNewDeviconJson(colorsMap);
}

/**
 * Create a map of technology name and their corresponding 
 * colors by parsing the devicon.css.
 * @return an object that maps technology name to colors.
 */
function constructColorsMap() {
	let filePath = path.join(__dirname, "devicon-colors.css");
	let css = fs.readFileSync(filePath, "utf8");
	let key = null;
	let deviconColors = {};
	css.split("\n").forEach(line => {
		if (key) {
			// since have key, now look for line
			// that contains 'color: ###'
			if (line.match(/color: /)) {
				deviconColors[key] = line.match(/#\w+/)[0];
				key = null;
			}
			return;
		}

		if (line.match(/devicon/)) {
			key = line.match(/-\w+/)[0].slice(1);
		}
	});
	return deviconColors;
}

/**
 * Create a new devicon.json that contains font objects
 * with the color attributes.
 * @param {Object} colorsMap 
 */
function createNewDeviconJson(colorsMap) {
	let deviconPath = path.join(__dirname, "devicon.json");
	let deviconJson = JSON.parse(fs.readFileSync(deviconPath, "utf8"));

	let newDeviconJson = deviconJson.map(font => addColorToObj(font, colorsMap));
	let newDeviconJsonPath = path.join(__dirname, "newDevicon.json");
	fs.writeFileSync(newDeviconJsonPath,
		JSON.stringify(newDeviconJson), "utf8");
}

/**
 * Add the correct color attribute to the fontObject by 
 * parsing through the colorsMap.
 * @param {Object} fontObj a font object from the devicon.json.
 * @param {Object} colorsMap the colorsMap create by constructColorsMap()
 */
function addColorToObj(fontObj, colorsMap) {
	try {
		let key = fontObj.name;
		fontObj["color"] = colorsMap[key];
	} catch(err) {
		console.log(err);
		console.log(`Font ${fontObj.name} doesn't exist in colorsMap`)
	} finally {
		return fontObj;
	}

}

main();