import sublime, sublime_plugin
import webbrowser
import os, subprocess
import platform
from urllib.parse import urlparse, urlencode

# Define a startupinfo which can be passed to subprocess calls which hides the
# command prompt on Windows. Otherwise doing simple things like e.g. running a
# git command would create a visual Command Prompt window, annoying the user.
startupinfo = None
if platform.system() == 'Windows':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

VERSION = 'v1.0.3'
FILENAME_SETTINGS = 'Sourcegraph.sublime-settings'

# gitRemotes returns the names of all git remotes, e.g. ['origin', 'foobar']
def gitRemotes(repoDir):
	proc = subprocess.Popen(['git', 'remote'], stdout=subprocess.PIPE, cwd=repoDir, startupinfo=startupinfo)
	return proc.stdout.read().decode('utf-8').splitlines()

# gitRemoteURL returns the remote URL for the given remote name.
# e.g. 'origin' -> 'git@github.com:foo/bar'
def gitRemoteURL(repoDir, remoteName):
	proc = subprocess.Popen(['git', 'remote', 'get-url', remoteName], stdout=subprocess.PIPE, cwd=repoDir, startupinfo=startupinfo)
	return proc.stdout.read().decode('utf-8').rstrip()

# gitDefaultRemoteURL returns the remote URL of the first Git remote found. An
# exception is raised if there is not one.
def gitDefaultRemoteURL(repoDir):
	remotes = gitRemotes(repoDir)
	if len(remotes) == 0:
		raise Exception('no configured git remotes')
	if len(remotes) > 1:
		print('using first git remote:', remotes[0])
	return gitRemoteURL(repoDir, remotes[0])

# gitRootDir returns the repository root directory for any directory within the
# repository.
def gitRootDir(repoDir):
	proc = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, cwd=repoDir, startupinfo=startupinfo)
	return proc.stdout.read().decode('utf-8').rstrip()

# gitBranch returns either the current branch name of the repository OR in all
# other cases (e.g. detached HEAD state), it returns "HEAD".
def gitBranch(repoDir):
	proc = subprocess.Popen(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE, cwd=repoDir, startupinfo=startupinfo)
	return proc.stdout.read().decode('utf-8').rstrip()

# removePrefixes removes any of the given prefixes from the input string `s`.
# Only one prefix is removed.
def removePrefixes(s, prefixes):
	for p in prefixes:
		if s.startswith(p):
			return s[len(p):]
	return s

# replaceLastOccurrence returns `s` with the last occurrence of `a` replaced by
# `b`.
def replaceLastOccurrence(s, a, b):
	k = s.rfind(a)
	if k == -1:
		return s
	return s[:k] + b + s[k+1:]

# repoFromRemoteURL returns the repository name from the remote URL. An
# exception is raised if it cannot be determined. Supported formats are:
#
# 	optional("ssh://" OR "git://" OR "https://" OR "https://")
# 	+ optional("username") + optional(":password") + optional("@")
# 	+ "github.com"
# 	+ "/" OR ":"
# 	+ "<organization>" + "/" + "<username>"
#
def repoFromRemoteURL(remoteURL):
	# Normalize all URL schemes into 'http://' just for parsing purposes. We
	# don't actually care about the scheme itself.
	r = removePrefixes(remoteURL, ['ssh://', 'git://', 'https://', 'http://'])

	# Normalize github.com:foo/bar -> github.com/foo/bar -- Note we only do the
	# last occurrence as it may be included earlier in the case of 'foo:bar@github.com'
	r = replaceLastOccurrence(r, ':', '/')

	u = urlparse('http://' + r)
	if not u.netloc.endswith('github.com'): # Note: using endswith because netloc may have 'username:password@' prefix.
		raise Exception('repository remote is not github.com', remoteURL)
	return 'github.com' + u.path

def sourcegraphURL(settings):
	sourcegraphURL = settings.get('SOURCEGRAPH_URL')
	if not sourcegraphURL.endswith('/'):
		return sourcegraphURL + '/'
	return sourcegraphURL

def lineHash(row, col, row2, col2):
	return 'L' + str(row+1) + ':' + str(col+1) + '-' + str(row2+1) + ':' + str(col2+1)

def branchStr(branch):
	if branch == 'HEAD':
		return '' # Detatched head state
	if branch == 'master':
		# Assume master is the default branch, for now.
		return ''
	return '@' + branch

# repoInfo returns the Sourcegraph repository URI, and the file path relative
# to the repository root. If the repository URI cannot be determined, an
# exception is logged and (None, None) is returned.
def repoInfo(fileName):
	repo = None
	fileRel = None
	branch = None
	try:
		# Determine repository root directory.
		fileDir = os.path.dirname(fileName)
		repoRoot = gitRootDir(fileDir)

		# Determine file path, relative to repository root.
		fileRel = fileName[len(repoRoot)+1:]
		repo = repoFromRemoteURL(gitDefaultRemoteURL(repoRoot))
		branch = gitBranch(repoRoot)
	except Exception as e:
		print("repoInfo:", e)
	return repo, branch, fileRel

class SourcegraphOpenCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		repo, branch, fileRel = repoInfo(self.view.file_name())
		if repo == None:
			return

		# For now, we assume the first selection is the most interesting one.
		(row,col) = self.view.rowcol(self.view.sel()[0].begin())
		(row2,col2) = self.view.rowcol(self.view.sel()[0].end())

		# Open in browser
		settings = sublime.load_settings(FILENAME_SETTINGS)
		url = sourcegraphURL(settings) + repo + branchStr(branch) + '/-/blob/' + fileRel + '?' + urlencode({'utm_source': 'Sublime-' + VERSION}) + '#' + lineHash(row, col, row2, col2)
		webbrowser.open(url, new=2)

class SourcegraphSearchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# For now, we assume the first selection is the most interesting one.
		(row,col) = self.view.rowcol(self.view.sel()[0].begin())
		(row2,col2) = self.view.rowcol(self.view.sel()[0].end())
		query = self.view.substr((self.view.sel())[0])
		if query == '':
			return # nothing to query

		# Search in browser
		settings = sublime.load_settings(FILENAME_SETTINGS)
		url = sourcegraphURL(settings) + 'search' + '?' + urlencode({'q': query, 'utm_source': 'Sublime-' + VERSION})
		webbrowser.open(url, new=2)
