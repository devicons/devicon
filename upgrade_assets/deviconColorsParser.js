/* Parse the devicon-colors.css and convert it to devicon-colors.json*/
const fs = require("fs");
const path = require('path');

function main() {
	let filePath = path.join(__dirname, "..", "css", "devicon-colors.css");
	fs.readFile(filePath, "utf8", (err, css) => {
		if (err) {
			console.log(err);
			return;
		}

		let key = null;
		let deviconColors = {};
		css.split("\n").forEach(line => {
			if (key) {
				// since have key, now look for line
				// that contains color: ###
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

		let deviconColorsFile = path.join(__dirname, "deviconColors.json");
		fs.writeFile(deviconColorsFile, JSON.stringify(deviconColors), err => {
			console.log(err ? err : "File successfully created");
		})
	});

}

main();