`JS module to implement basic Trie data structure`;

class TrieST {
  // R size set to cater for all ASCII chars
  #R = 256;
  #root = null;

  constructor() {
    this.value = null;
  }
  /**
   * Method to initialize trie node with null links
   * @param {Boolean} is_root True if value to be initialise is root
   * @returns {TrieST}
   */
  init(is_root = false) {
    this.next = [...Array(this.#R)].fill(null);

    if (is_root) this.#root = this;
    return this;
  }

  /**
   * Find given key in trie
   * @param {TrieST | null} s_node Start node, usually root
   * @param {String} key Key to be searched for
   * @param {Number} i Start index
   * @returns {Number | null}
   */
  get(s_node, key, i = 0) {
    if (s_node === null) return null;

    if (i === key.length) {
      return s_node === this.#root || s_node.value !== null ? s_node : null;
    }

    let c = key.charCodeAt(i);
    let value = this.get(s_node.next[c], key, i + 1);

    return value;
  }

  /**
   * Method to add a key to the trie
   * @param {TrieST | null} s_node Start node, usually root
   * @param {String} key Key to be inserted
   * @param {Number} value value to be associated with key
   * @param {Number} i=0 indexing variable
   * @returns {TrieST}
   */
  put(s_node, key, value, i = 0) {
    if (s_node === null) {
      s_node = new TrieST().init();
    }

    // At end of key, associate value assigned with last char
    if (i === key.length) {
      s_node.value = value;
      return s_node;
    }

    // Get ASCII value of character at current index i
    let c = key.charCodeAt(i);

    s_node.next[c] = this.put(s_node.next[c], key, value, i + 1);
    return s_node;
  }
}

module.exports = { TrieST };
