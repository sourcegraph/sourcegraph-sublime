# Sourcegraph for Sublime Text 3

## Installation

1. [Install Package Control](https://packagecontrol.io/installation), if you haven't already.
1. Open the command palette `Cmd+Shift+P` (`Ctrl+Shift+P` on Windows/Linux).
2. Search for `Package Control: Install Package` and press enter.
3. Search for `Sourcegraph` and press enter to install the plugin.


## Usage

In the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`), search for `Sourcegraph:` to see available actions.

Keyboard Shortcuts:

| Description                     | Mac        | Linux / Windows |
|---------------------------------|------------|-----------------|
| Open file in Sourcegraph        | `Option+O` | `Alt+O`         |
| Search selection in Sourcegraph | `Option+K` | `Alt+K`         |


## Questions & Feedback

Please file an issue: https://github.com/sourcegraph/sourcegraph-sublime/issues/new


## Logs

Logs show up in the Sublime console, which is accessible via ``` Ctrl+` ``` (ctrl+backtick)


## Uninstallation

1. Open the command palette `Cmd+Shift+P` (`Ctrl+Shift+P` on Windows/Linux).
2. Search for `Package Control: Remove Package` and press enter.
3. Search for `sourcegraph` and press enter to uninstall the plugin.


## Development

To develop the plugin:

- `git clone` the repository into `~/Library/Application Support/Sublime Text 3/Packages/sourcegraph-sublime`
- Open the console with ``` `Ctrl+` ``` (ctrl+backtick)
- Make changes to the Python code and watch as Sublime reloads.
- To release a new version: update `messages.json`, `README.md`, and `messages/welcome.txt` and commit; then `git tag v0.0.0` and `git push --tags`.

## Version History

- v1.0.1 - minor bug fixes
    - Fixed a bug where `https` etc. GitHub repo remote URLs would incorrectly build the Sourcegraph.com URL.
    - Windows: Fixed a bug where git commands would create Command Prompt pop-up windows.

- v1.0.0 - Initial Release; basic Open File & Search functionality.
