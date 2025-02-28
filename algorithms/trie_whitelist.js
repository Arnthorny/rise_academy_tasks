`Basic file based whitelist using a trie`;

const readline = require("readline");
const fs = require("fs");
const TrieST = require("./tries.js").TrieST;

const trie_root = new TrieST().init((is_root = true));

// Get Whitelist file from command line and read into variable
const whitelistFile = process.argv[2];
const whitelistFileStr = fs.readFileSync(whitelistFile).toString();

// Populate trie with words from whitelist file
whitelistFileStr.split(" ").forEach((word, idx) => {
  trie_root.put(trie_root, word, idx);
});

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
    if (trie_root.get(trie_root, word) !== null) {
      process.stdout.write(`${word} `);
    }
  });
});

rl.once("close", () => {
  console.log();
});
