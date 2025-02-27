const readline = require("readline");
const fs = require("fs");

// Get Whitelist file from command line and read into variable
const whitelistFile = process.argv[2];
const whitelistFileStr = fs.readFileSync(whitelistFile).toString();

// Create set object from whitelist file
const setWl = new Set(whitelistFileStr.split(" "));

const setVal = new Set();

// Create a readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false,
});

// Read each line from stdin and split into whitespaced words
rl.on("line", (line) => {
  const all_words = line.split(" ");

  all_words.forEach((word) => {
    if (setWl.has(word)) {
      setVal.add(word);
      process.stdout.write(`${word} `);
    }
  });
});

rl.once("close", () => {
  console.log();
});
