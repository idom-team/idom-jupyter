var widgets = require("@jupyter-widgets/base");
var _ = require("lodash");

var IdomModel = widgets.DOMWidgetModel.extend({
  defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
    _model_name: "IdomModel",
    _view_name: "IdomView",
    _model_module: "idom-client-jupyter",
    _view_module: "idom-client-jupyter",
    _model_module_version: "0.4.0",
    _view_module_version: "0.4.0",
    _jupyter_server_base_url: null,
  }),
});

var _nextViewID = { id: 0 };

class IdomView extends widgets.DOMWidgetView {
  constructor(options) {
    super(options);
    this.render = this.render.bind(this);
    this.remove = this.remove.bind(this);
  }

  render() {
    this.viewID = _nextViewID.id;
    _nextViewID.id++;

    var saveUpdateHook = (updateHook) => {
      this.model.on("msg:custom", (msg, buffers) => {
        if (msg.viewID == this.viewID) {
          updateHook(...msg.data);
        }
      });
      this.model.send({
        type: "client-ready",
        viewID: this.viewID,
        data: null,
      });
    };

    var sendEvent = (event) => {
      this.model.send({ type: "dom-event", viewID: this.viewID, data: event });
    };

    const idomWebModulesUrl = concatAndResolveUrl(
      this.model.attributes._jupyter_server_base_url ||
        getJupyterServerBaseUrl(),
      "_idom_web_modules"
    );
    const idomClientReactUrl = concatAndResolveUrl(
      idomWebModulesUrl,
      "idom-client-react.js"
    );
    eval(`import('${idomClientReactUrl}')`).then((module) =>
      module.mountLayout(this.el, saveUpdateHook, sendEvent, idomWebModulesUrl)
    );
  }

  remove() {
    this.send({ type: "client-removed", viewID: this.viewID });
    return super.remove();
  }
}

function getJupyterServerBaseUrl() {
  const jupyterConfig = document.getElementById("jupyter-config-data");
  if (jupyterConfig) {
    return JSON.parse(jupyterConfig.text)["baseUrl"];
  }
  return document.getElementsByTagName("body")[0].getAttribute("data-base-url");
}

function concatAndResolveUrl(url, concat) {
  var url1 = (url.endsWith("/") ? url.slice(0, -1) : url).split("/");
  var url2 = concat.split("/");
  var url3 = [];
  for (var i = 0, l = url1.length; i < l; i++) {
    if (url1[i] == "..") {
      url3.pop();
    } else if (url1[i] == ".") {
      continue;
    } else {
      url3.push(url1[i]);
    }
  }
  for (var i = 0, l = url2.length; i < l; i++) {
    if (url2[i] == "..") {
      url3.pop();
    } else if (url2[i] == ".") {
      continue;
    } else {
      url3.push(url2[i]);
    }
  }
  return url3.join("/");
}

module.exports = {
  IdomModel: IdomModel,
  IdomView: IdomView,
};
