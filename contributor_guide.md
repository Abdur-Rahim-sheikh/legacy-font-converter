### Help the child package to grow into a full-fledged package and contribute to the community

We are looking for contributors to help us grow the child package into a full-fledged package and contribute to the community. We are open to all kinds of contributions, be it bug fixes, enhancements, documentation improvements, or any other help that you can provide. We value all the contributions and we will be happy to add you as a contributor.

### Two main ways to contribute
1. Attach a json file containing new legacy font converter mapping legacy to unicode in the `issue` section in the following format:
```json
{
    "find": "list[str] the legacy font patterns",
    "replace": "list[str] the unicode equivalent of the legacy font pattern at the same index"
}
```

2. Fork the repository, add your changes just putting the above mentioned json file in the `legacy_font_converter/resources` build the package and test it locally. If everything is working fine, create a pull request. You can follow the build procedure [below](#build-procedure).

### Let me tell you how this package works
1. First i take each json file located in the `legacy_font_converter/resources` directory and load it into my code.
2. I have created a special trie class which is built upon these json file.
    - It maintains pattern precedence, so if in the list of "find" patterns, the first pattern is found in the text, it will be replaced by the first pattern in the "replace" list.
    - It also handles prefix issue and gives the priority to the lowest index pattern.
    - The project is inspired from [True finder studio](https://github.com/truefinderstudio), but their code works with O(text_length * number_of_patterns) complexity, which is not efficient. I have optimized it to O(text_length) complexity.
    - The trie is itself fine invention which comes with the package `from legacy_font_converter import SpecialTrie`
    - It takes two list of strings, one for "find" and other for "replace" and builds a trie out of it. And if you call `trie_instance.find(text)` it will return the text with the patterns replaced.

### Build procedure
1. Clone the repository
2. Place the json file in the `legacy_font_converter/resources` directory
3. file should be named after the font name ie `sutonnymj.json`
4. Run the following command to build the package
```bash
poetry build
```
