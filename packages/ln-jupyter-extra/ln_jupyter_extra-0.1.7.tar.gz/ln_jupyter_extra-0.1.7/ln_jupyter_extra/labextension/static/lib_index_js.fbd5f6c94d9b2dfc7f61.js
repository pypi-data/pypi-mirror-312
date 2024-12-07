"use strict";
(self["webpackChunkln_jupyter_extra"] = self["webpackChunkln_jupyter_extra"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__);



// import createVersion from './widgets/createVersion';
// import VersionListSidebarWidget from './widgets/version';
// import DataSetListSidebarWidget from './widgets/dataset';
// import UsageTimeWidget from './widgets/time';
// // import LogMonitorWidget from './widgets/log';
// import TitleWidget from './widgets/title';
// import { getProjectDetail } from './api/project';
// import { Notification } from '@jupyterlab/apputils';
// import VariableInspectorPlugins from './widgets/variable/index';
/**
 * Activate the ln-notebook extension.
 *
 * @param app - The JupyterLab Application instance
 * @param palette - The command palette instance
 * @param restorer - The application layout restorer
 * @param statusBar - The status bar instance
 *
 * @returns A promise that resolves when the extension has been activated
 */
async function activate(app, palette, restorer, statusBar, router) {
    var _a;
    console.log('JupyterLab extension ln-jupyter-extra is activating!');
    // 检查路由对象是否正常
    if (!router) {
        console.error('Router is undefined. Ensure IRouter is properly declared in "requires".');
        return;
    }
    console.log('Router object:', router);
    // 监听路由变化
    router.routed.connect((_, args) => {
        console.log('Route initialized or changed:', args.path);
    });
    // 延迟访问路由信息
    setTimeout(() => {
        var _a;
        console.log('Delayed Current route:', ((_a = router.current) === null || _a === void 0 ? void 0 : _a.path) || 'Route not ready');
    }, 1000);
    console.log('Initial route:', ((_a = router.current) === null || _a === void 0 ? void 0 : _a.path) || 'Route not ready');
    // 插件其他初始化逻辑
    console.log('JupyterLab extension ln-jupyter-extra activated successfully!');
}
const lnPlugin = {
    id: 'ln-notebook:plugin',
    description: 'leinao extra jupyter plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__.IStatusBar],
    activate: activate
};
const plugins = [lnPlugin];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.fbd5f6c94d9b2dfc7f61.js.map