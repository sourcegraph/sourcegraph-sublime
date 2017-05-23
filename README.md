# Sourcegraph for Sublime Text 3 [![Package Control](https://img.shields.io/packagecontrol/dt/Sourcegraph.svg)](https://packagecontrol.io/packages/Sourcegraph)

The Sourcegraph plugin for Sublime Text 3 enables you to quickly open and search code on Sourcegraph.com easily and efficiently.

## Installation

1. [Install Package Control](https://packagecontrol.io/installation), if you haven't already.
1. Open the command palette <kbd>Cmd+Shift+P</kbd> (<kbd>Ctrl+Shift+P</kbd> on Windows/Linux).
2. Search for `Package Control: Install Package` and press enter.
3. Search for `Sourcegraph` and press enter to install the plugin.


## Usage

In the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`), search for `Sourcegraph:` to see available actions.

Keyboard Shortcuts:

| Description                     | Mac                 | Linux / Windows  |
|---------------------------------|---------------------|------------------|
| Open file in Sourcegraph        | <kbd>Option+A</kbd> | <kbd>Alt+A</kbd> |
| Search selection in Sourcegraph | <kbd>Option+S</kbd> | <kbd>Alt+S</kbd> |


## Settings

Open the user package settings (`Sublime Text` -> `Package Settings` -> `Sourcegraph` -> `Settings - User`), then modify this example configuration:

```
{
	// The Sourcegraph instance to use. Specify your on-premises Sourcegraph
	// instance here, if applicable.
	"SOURCEGRAPH_URL": "https://sourcegraph.com",
}
```


## Questions & Feedback

Please file an issue: https://github.com/sourcegraph/sourcegraph-sublime/issues/new


## Logs

Logs show up in the Sublime console, which is accessible via <kbd>Ctrl+`</kbd>


## Uninstallation

1. Open the command palette <kbd>Cmd+Shift+P</kbd> (<kbd>Ctrl+Shift+P</kbd> on Windows/Linux).
2. Search for `Package Control: Remove Package` and press enter.
3. Search for `sourcegraph` and press enter to uninstall the plugin.


## Development

To develop the plugin:

- `git clone` the repository into `~/Library/Application Support/Sublime Text 3/Packages/sourcegraph-sublime`
- Open the console with <kbd>Ctrl+`</kbd>
- Make changes to the Python code and watch as Sublime reloads.
- To release a new version, you MUST update the following files:
  1. `messages.json` (add a new version entry)
  2. `README.md` (describe ALL changes)
  3. `messages/welcome.txt` (copy from README.md change above)
  4. `sourcegraph.py` (`VERSION` constant)
  - Then `git commit -m "all: release v<THE VERSION>` and `git push` and `git tag v<THE VERSION>` and `git push --tags`.
  - Note: it sometimes takes a few hours for it to show up on https://packagecontrol.io/packages/Sourcegraph


## Version History

- v1.0.4 - Improved support for on-premises Sourcegraph instances
    - Now using the `sourcegraph.com/-/editor` endpoint.

- v1.0.3 - Added usage metrics
    - Added minimal and non-obtrusive usage metrics, which lets us at Sourcegraph better improve our editor extensions.

- v1.0.2 - Usability improvements
    - Adjusted the global search URL to the correct one, so that the search shortcut will work.
    - Added support for non-default git branches (brings you to the checked out branch on Sourcegraph.com)
    - Changed the keyboard shortcuts to <kbd>Option+S</kbd> (search selection) and <kbd>Option+A</kbd> (open selection) (<kbd>Alt</kbd> instead of <kbd>Option</kbd> for Windows and Linux).

- v1.0.1 - Minor bug fixes
    - Fixed a bug where `https` etc. GitHub repo remote URLs would incorrectly build the Sourcegraph.com URL.
    - Windows: Fixed a bug where git commands would create Command Prompt pop-up windows.

- v1.0.0 - Initial Release; basic Open File & Search functionality.
