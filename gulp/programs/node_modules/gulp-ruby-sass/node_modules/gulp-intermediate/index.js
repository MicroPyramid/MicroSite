'use strict';

var fs = require('fs');
var path = require('path');
var uuid = require('uuid');
var glob = require('glob');
var gutil = require('gulp-util');
var mkdirp = require('mkdirp');
var rimraf = require('rimraf');
var osTempDir = require('os').tmpdir();
var Transform = require('stream').Transform;

module.exports = function (options, process) {
  options = options || {};
  var outputDir = options.output || '.';
  var container = options.container || uuid.v4();
  var transform = new Transform({ objectMode: true });
  var tempDir = path.join(osTempDir, container);
  var origCWD;
  var origBase;

  if (options.container) {
    rimraf.sync(tempDir);
  }

  transform._transform = function(file, encoding, cb) {
    var self = this;
    var tempFilePath = path.join(tempDir, file.relative);
    var tempFileBase = path.dirname(tempFilePath);

    if (!origCWD) {
      origCWD = file.cwd;
    }

    if (!origBase) {
      origBase = file.base;
    }

    if (file.isNull()) {
      this.push(file);
      return cb();
    }

    if (file.isStream()) {
      this.emit('error', new gutil.PluginError('gulp-intermediate', 'Streaming not supported'));
      return cb();
    }

    mkdirp(tempFileBase, function (err) {
      if (err) {
        self.emit('error', new gutil.PluginError('gulp-intermediate', err));
        return cb();
      }

      fs.writeFile(tempFilePath, file.contents, function(err)  {
        if (err) {
          self.emit('error', new gutil.PluginError('gulp-intermediate', err));
          return cb();
        }

        if (file.stat && file.stat.atime && file.stat.mtime) {
          fs.utimes(tempFilePath, file.stat.atime, file.stat.mtime, function(err)  {
            if (err) {
              self.emit('error', new gutil.PluginError('gulp-intermediate', err));
              return cb();
            }

            cb();
          });
        }
        else {
          cb();
        }
      });
    });
  };

  transform._flush = function(cb) {
    var self = this;

    process(tempDir, function(err) {
      if (err) {
        self.emit('error', new gutil.PluginError('gulp-intermediate', err));
        return cb();
      }

      glob('**/*', { cwd: path.join(tempDir, outputDir) }, function (err, files) {
        if (err) {
          self.emit('error', new gutil.PluginError('gulp-intermediate', err));
          return cb();
        }

        files.forEach(function (file) {
          var realPath = path.join(tempDir, outputDir, file);

          // TODO: Can we make readFile async?
          if (fs.statSync(realPath).isFile()) {
            self.push( new gutil.File({
              cwd: origCWD,
              base: origBase,
              path: path.join(origBase, file),
              contents: new Buffer(fs.readFileSync(realPath))
            }));
          }
        });

        cb();
      });
    }, { cwd: origCWD });
  };

  return transform;
};
