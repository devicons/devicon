const fs = require("fs");
const path = require('path');

// the standard css statement is .devicon-{name}-{version} {content: ""}
// this extract the {name}-{version}. This is greedy => will match
// react-original, dot-net-original and mocha
const TECH_NAME_REG_EXP = /(?<=-)(\w+-)*\w+/ig;
// this extract the ""
const CONTENT_REG_EXP = /(?<=")\\\w+(?=")/;

function main() {
	let contentMap = constructDeviconContentMap();
	let aliasMap = constructAliasContentMap();
	let colorsMap = constructColorsMap();

	// if you want to see what the maps are like
	// fs.writeFileSync(path.join(__dirname, "contentMap.json"),
	// 	JSON.stringify(contentMap), "utf8");
	// fs.writeFileSync(path.join(__dirname, "aliasMap.json"),
	// 	JSON.stringify(aliasMap), "utf8");
	// fs.writeFileSync(path.join(__dirname, "colorsMap.json"),
	// 	JSON.stringify(colorsMap), "utf8");

	createNewDeviconJson(colorsMap, contentMap, aliasMap);
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
			key = line.match(/(?<=-)\w+/)[0];
		}
	});
	return deviconColors;
}

/**
 * Create a map of technology name and their corresponding 
 * content string by parsing the devicon.css.
 * @return an object that maps technology name to content string.
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
 * technology name to the content string.
 */
function getNameAndContentFromStr(str, contentMap) {
    try {
        let techName = str.match(TECH_NAME_REG_EXP)[0];
        let content = str.match(CONTENT_REG_EXP)[0];
        contentMap[techName] = content;
    } catch(e) {
        console.log(str);
        console.error(e);
    }
}

/**
 * Create a map of contents mapped to aliases
 * by parsing the devicon-alias.css.
 * @return an object that maps content string to an array of 
 * aliases name.
 */
function constructAliasContentMap() {
	let filePath = path.join(__dirname, "devicon-alias.css");
	let css = fs.readFileSync(filePath, "utf8");
	let deviconAliases = {};
	css.match(/\.devicon-(.*\s+){2,}?(?=})/g).forEach(str => 
		getAliasAndContentFromStr(str, deviconAliases));
	return deviconAliases;
}

/**
 * Get the aliases and content from the str and
 * put them in the aliasMap.
 * @param {String} str, a css selector str 
 * @param {Object} aliasMap, an object that maps the
 * content string to an array of class names/aliases.
 */
function getAliasAndContentFromStr(str, aliasMap) {
	let techNames = str.match(TECH_NAME_REG_EXP);
	let content = str.match(CONTENT_REG_EXP)[0];
	aliasMap[content] = techNames;
}

/**
 * Create a new devicon.json that contains font objects
 * with the color attributes.
 * @param {Object} colorsMap the colorsMap create by constructColorsMap()
 * @param {Object} contentMap the contentMap create by constructDeviconContentMap()
 * @param {Object} aliasMap the aliasMap create by constructAliasContentMap()
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

	// run check to ensure every object has the needed attribute
    // log all fonts that are missing a color or don't have an array
	// let specialFont = newDeviconJson.filter(fontObj => {
	// 	return !(typeof(fontObj["color"]) === "string"
	// 		&& Array.isArray(fontObj["aliases"]));
	// })

	// console.log(specialFont);
}

/**
 * Add the correct 'color' attribute to the fontObject by 
 * parsing through the colorsMap.
 * @param {Object} fontObj a font object from the devicon.json.
 * @param {Object} colorsMap the colorsMap create by constructColorsMap()
 */
function addColorToObj(fontObj, colorsMap) {
	let key = fontObj.name;
	if (colorsMap[key]) {
		fontObj["color"] = colorsMap[key];
	} else {
		console.log(`This font doesn't have a color: ${key}. Skipping it`)
	}
	return fontObj;
}

/**
 * Add the correct 'aliases' attribute to the fontObject by 
 * parsing through the colorsMap.
 * @param {Object} fontObj a font object from the devicon.json.
 * @param {Object} contentMap the contentMap create by constructDeviconContentMap()
 * @param {Object} aliasMap the aliasMap create by constructAliasContentMap()
 */
function addAliasesToObj(fontObj, contentMap, aliasMap) {
	fontObj["aliases"] = [];

	// the contentMap contains the mappings of the base versions
	// the aliasMap contains the mappings of the alias versions
	let fontNames = fontObj["versions"]["font"].map(version => {
		return `${fontObj["name"]}-${version}`;
	});

	// for each font version, we check if it has an entry in
	// the content map. If it does, check if that content has an alias(es)
	// If that also pass, we construct the alias object based on those info.
	for (let fontName of fontNames) {
		let content = contentMap[fontName];
		if (typeof(content) !== "string") continue;

		let aliases = aliasMap[content];
		if (!Array.isArray(aliases)) continue;

		let aliasObjs = aliases.map(alias => {
			return {
				"base": extractVersion(fontName),
				"alias": extractVersion(alias)
			};
		});
		fontObj["aliases"] = fontObj["aliases"].concat(aliasObjs);
	}
	return fontObj;
}

/**
 * Extract the font version from a font name.
 * @param {string} fontName, a font name in the format of
 * "techname"-"version".
 * @return the font version as a string ("original", "plain", etc..)
 */
function extractVersion(fontName) {
	let fontVersioRegExp = /(original|plain|line)(-wordmark)?/;
	return fontName.match(fontVersioRegExp)[0];
}

main();