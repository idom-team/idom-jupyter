var plugin = require("./index");
var base = require("@jupyter-widgets/base");

module.exports = {
  id: "idom-client-jupyter",
  requires: [base.IJupyterWidgetRegistry],
  activate: function (app, widgets) {
    widgets.registerWidget({
      name: "idom-client-jupyter",
      version: plugin.version,
      exports: plugin,
    });
  },
  autoStart: true,
};
