// soledad penades www.soledadpenades.com

const process = require('node:process');
const path = require('node:path');
const fs = require('node:fs');
const argv = process.argv;

let folder;

// something something I don't need like .../bin/node
if(process.execPath === argv[0]) {
	argv.splice(0, 1);
}

// remaining is this script name and hopefully a destination folder name
if(argv.length > 1) {
	folder = argv[1];
} else {
	console.error("Specify destination folder to be split");
	process.exit(-1);
}

console.log(`Splitting ${folder}`);

let dstPath = folder;

if(!path.isAbsolute(dstPath)) {
	dstPath = path.resolve('.', dstPath);
	console.log(`Resolving to ${dstPath}`);
}

fs.readdirSync(dstPath, { withFileTypes: true }).forEach((item) => {
	let itemPath = path.join(dstPath, item.name);
	console.log(itemPath);

	// Leave directories alone - move only files
	if(item.isDirectory()) {
		console.log(`Skipping ${item.name} as it's a directory`);
		return;
	} 
	
	let s = fs.statSync(itemPath);
	let ctime = s.ctimeMs;
	let mtime = s.mtimeMs;
	let finalTime;

	if(ctime > mtime) {
		finalTime = s.mtime;
	} else {
		finalTime = s.ctime;
	}

	//let finalTime = Math.min(s.ctimeMs, s.mtimeMs);
	let finalDate = new Date(finalTime);
	let day = finalDate.getDate();
	let month = finalDate.getMonth() + 1; // 0 index based
	let year = finalDate.getFullYear();

	day = String(day).padStart(2, '0');
	month = String(month).padStart(2, '0');

	let subFolder = `${year}${month}${day}`;
	
	console.log(finalDate, year, month, day, subFolder);

	let subFolderPath = path.join(dstPath, subFolder);

	if(!fs.existsSync(subFolderPath)) {
		console.log(`${subFolder} does not exist yet, creating`);
		fs.mkdirSync(subFolderPath);
	}

	let newItemPath = path.join(subFolderPath, item.name);

	console.log(`${itemPath} => ${newItemPath}`);

	fs.renameSync(itemPath, newItemPath);

});
