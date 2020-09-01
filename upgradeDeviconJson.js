/* Parse the devicon-colors.css and convert it to devicon-colors.json*/
const fs = require("fs");
const path = require('path');
const techNameRegExp = /(?<=-)(\w+-)+\w+/ig;
const contentRegExp = /(?<=")\\\w+(?=")/;

function main() {
	let contentMap = constructDeviconContentMap();
	let aliasMap = constructAliasContentMap();
	let colorsMap = constructColorsMap();
	createNewDeviconJson(colorsMap, contentMap, aliasMap);
	// fs.writeFileSync(path.join(__dirname, "devContent.json"), JSON.stringify(contentMap));
	// fs.writeFileSync(path.join(__dirname, "devAliasContent.json"), JSON.stringify(aliasMap));
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
 * Create a map of technology name and their corresponding 
 * colors by parsing the devicon.css.
 * @return an object that maps technology name to colors.
 */
function constructDeviconContentMap() {
	let filePath = path.join(__dirname, "devicon.css");
	let css = fs.readFileSync(filePath, "utf8");
	let deviconContent = {};
	css.match(/\.devicon-(.*\s+){2,}?(?=})/g).forEach(str => 
		getNameAndContentFromStr(str, deviconContent));
	return deviconContent;
}


/**
 * Get the class name and content from the str and
 * put them in the contentMap.
 * @param {String} str, a css selector str 
 * @param {Object} contentMap, an object that maps the
 * class name to the content.
 */
function getNameAndContentFromStr(str, contentMap) {
	let techName = str.match(techNameRegExp)[0];
	let content = str.match(contentRegExp)[0];
	contentMap[techName] = content;
}

/**
 * Create a map of technology name and their corresponding 
 * colors by parsing the devicon-alias.css.
 * @return an object that maps technology name to colors.
 */
function constructAliasContentMap() {
	let filePath = path.join(__dirname, "devicon-alias.css");
	let css = fs.readFileSync(filePath, "utf8");
	let deviconContent = {};
	css.match(/\.devicon-(.*\s+){2,}?(?=})/g).forEach(str => 
		getAliasAndContentFromStr(str, deviconContent));
	return deviconContent;
}

/**
 * Get the aliases and content from the str and
 * put them in the aliasMap.
 * @param {String} str, a css selector str 
 * @param {Object} aliasMap, an object that maps the
 * content to an array of class names/aliases.
 */
function getAliasAndContentFromStr(str, aliasMap) {
	let techNames = str.match(techNameRegExp);
	let content = str.match(contentRegExp)[0];
	aliasMap[content] = techNames;
}

/**
 * Create a new devicon.json that contains font objects
 * with the color attributes.
 * @param {Object} colorsMap the colorsMap create by constructColorsMap()
 * @param {Object} contentMap the colorsMap create by constructDeviconContentMap()
 * @param {Object} aliasMap the colorsMap create by constructAliasContentMap()
 */
function createNewDeviconJson(colorsMap, contentMap, aliasMap) {
	let deviconPath = path.join(__dirname, "devicon.json");
	let deviconJson = JSON.parse(fs.readFileSync(deviconPath, "utf8"));

	let newDeviconJson = deviconJson.map(font => {
		let newObj = addColorToObj(font, colorsMap);
		return addAliasesToObj(newObj, contentMap, aliasMap);
	});

	let newDeviconPath = path.join(__dirname, "newDevicon.json");
	fs.writeFileSync(newDeviconPath,
		JSON.stringify(newDeviconJson), "utf8");
}

/**
 * Add the correct 'color' attribute to the fontObject by 
 * parsing through the colorsMap.
 * @param {Object} fontObj a font object from the devicon.json.
 * @param {Object} colorsMap the colorsMap create by constructColorsMap()
 */
function addColorToObj(fontObj, colorsMap) {
	let key = fontObj.name;
	fontObj["color"] = colorsMap[key];
	return fontObj;
}

/**
 * Add the correct 'aliases' attribute to the fontObject by 
 * parsing through the colorsMap.
 * @param {Object} fontObj a font object from the devicon.json.
 * @param {Object} contentMap the colorsMap create by constructDeviconContentMap()
 * @param {Object} aliasMap the colorsMap create by constructAliasContentMap()
 */
function addAliasesToObj(fontObj, contentMap, aliasMap) {
	// the contentMap contains the mappings of the base versions
	// the aliasMap contains the mappings of the alias versions

}

main();