[![rsense](https://cloud.githubusercontent.com/assets/1395968/2978144/51565ee2-dbb5-11e3-9b94-e97a37739d03.png)](http://rsense.github.io/)

# rsense package

### [Rsense Can See All](http://rsense.github.io/)

[![Gitter chat](https://badges.gitter.im/rsense/rsense.png)](https://gitter.im/rsense/rsense)

RSense is a tool for doing static analysis of Ruby source code. Rsense is used in conjunction with an editor plugin. This is the plugin for the Atom editor.

RSense is currently in beta and ready for testing.  Currently we have exposed code-completion.  In the near future we'll also be ready to expose some of Rsense's other basic features like `find-definition`. After that, there's plenty to do in the long term.  See the waffle link below to find out where you can pitch in. It would be awesome if you helped get things done.

[![Stories in Ready](https://badge.waffle.io/rsense/rsense.png?label=ready&title=Ready)](https://waffle.io/rsense/rsense)

![A screenshot of your spankin' package](https://cloud.githubusercontent.com/assets/1395968/3344028/5b3c2f0a-f8a6-11e3-8952-c0f7155cb19e.gif)

## Installation

Add this line to your application's Gemfile:

    gem 'rsense'

And then execute:

    $ bundle

Or install it yourself as:

    $ gem install rsense

If you use `rbenv` please be sure to rehash: `rbenv rehash`.

Then install this package via [Sublime Text's package manager](https://sublime.wbond.net/), within preferences. Just search for `rsense`.

## Usage

You'll need to run `rsense start` from the command line, though we do eventually plan to add an command for starting and stopping the server.
You can tell RSense where your project is with `--path /path/to/project/root`.
The path passed in should be to the directory where your Gemfile is. This may improve the user experience.

Completions are triggered on `.` and `::`.

More information about rsense can be found at http://rsense.github.io/ .
