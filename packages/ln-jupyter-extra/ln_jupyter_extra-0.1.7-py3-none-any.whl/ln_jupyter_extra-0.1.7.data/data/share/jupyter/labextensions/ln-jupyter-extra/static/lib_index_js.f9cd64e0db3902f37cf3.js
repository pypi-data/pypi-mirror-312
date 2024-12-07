"use strict";
(self["webpackChunkln_jupyter_extra"] = self["webpackChunkln_jupyter_extra"] || []).push([["lib_index_js"],{

/***/ "./lib/api/project.js":
/*!****************************!*\
  !*** ./lib/api/project.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   addProjectVersion: () => (/* binding */ addProjectVersion),
/* harmony export */   getFileList: () => (/* binding */ getFileList),
/* harmony export */   getFileProxyToken: () => (/* binding */ getFileProxyToken),
/* harmony export */   getProjectDetail: () => (/* binding */ getProjectDetail),
/* harmony export */   getProjectVersionList: () => (/* binding */ getProjectVersionList)
/* harmony export */ });
/* harmony import */ var _request_index__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../request/index */ "./lib/request/index.js");

// const _baseUrlCommon = '/gateway/foundation/api/v1';
const _baseUrl = '/gateway/training/api/v1/notebook';
const _baseUrlToken = '/gateway/foundation/api/v1';
const _baseUrlFile = '/gateway/file-proxy/api/v1';
const getProjectVersionList = async (data) => {
    return await _request_index__WEBPACK_IMPORTED_MODULE_0__["default"].post(_baseUrl + '/version/action/page', {
        data
    });
};
/** 获取项目详情*/
const getProjectDetail = async (id) => {
    return await _request_index__WEBPACK_IMPORTED_MODULE_0__["default"].get(_baseUrl + '/project/' + id);
};
// 查询文件列表
const getFileList = async (data, authToken, clusterId = 'local') => {
    const headers = {
        Authorization: `Bearer ${authToken}`
    };
    const region = clusterId;
    return await _request_index__WEBPACK_IMPORTED_MODULE_0__.customRequest.get(_baseUrlFile + '/list', {
        params: { ...data, region },
        headers
    });
};
// 获取文件代理服务token（查询共享对象（模型或数据集）的文件token）
const getFileProxyToken = async (data) => {
    return await _request_index__WEBPACK_IMPORTED_MODULE_0__["default"].post(_baseUrlToken + '/shares/action/file/token', {
        data
    });
};
/** 新增版本 */
const addProjectVersion = async (data) => {
    return await _request_index__WEBPACK_IMPORTED_MODULE_0__["default"].post(_baseUrl + '/version', {
        data
    });
};


/***/ }),

/***/ "./lib/components/DatasetListPanel.js":
/*!********************************************!*\
  !*** ./lib/components/DatasetListPanel.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var lucide_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! lucide-react */ "webpack/sharing/consume/default/lucide-react/lucide-react");
/* harmony import */ var lucide_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(lucide_react__WEBPACK_IMPORTED_MODULE_1__);


const DatasetListPanel = ({ title, files, onFileClick = fileName => console.log(`Clicked file: ${fileName}`) }) => {
    const [isExpanded, setIsExpanded] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "ln-dataset-list-panel" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "panel-header", onClick: () => setIsExpanded(prev => !prev) },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "panel-title" }, title),
            isExpanded ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(lucide_react__WEBPACK_IMPORTED_MODULE_1__.ChevronDown, { size: 18, className: "icon" })) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(lucide_react__WEBPACK_IMPORTED_MODULE_1__.ChevronRight, { size: 18, className: "icon" }))),
        isExpanded && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { className: "file-list" }, files.length > 0 ? (files.map((file, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { key: `${file.fileName}-${index}`, className: "file-item", onClick: () => onFileClick(file.fileName) }, file.fileName)))) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: "no-files" }, "\u6682\u65E0\u6587\u4EF6"))))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DatasetListPanel);


/***/ }),

/***/ "./lib/components/VersionList.js":
/*!***************************************!*\
  !*** ./lib/components/VersionList.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VersionList: () => (/* binding */ VersionList)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var dayjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! dayjs */ "webpack/sharing/consume/default/dayjs/dayjs");
/* harmony import */ var dayjs__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(dayjs__WEBPACK_IMPORTED_MODULE_2__);



const VersionList = ({ version, createTime }) => {
    const handleVersionClick = () => {
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.success(`加载版本: ${version}`);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "ln-version-list-item" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "ln-version-list-item__name" }, version),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "ln-version-list-item__time" }, dayjs__WEBPACK_IMPORTED_MODULE_2___default()(createTime).format('YYYY-MM-DD HH:mm:ss'))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "ln-version-list-item__btn", onClick: handleVersionClick }, "\u52A0\u8F7D\u7248\u672C")));
};


/***/ }),

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
/* harmony import */ var _widgets_createVersion__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./widgets/createVersion */ "./lib/widgets/createVersion.js");
/* harmony import */ var _widgets_version__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widgets/version */ "./lib/widgets/version.js");
/* harmony import */ var _widgets_dataset__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widgets/dataset */ "./lib/widgets/dataset.js");
/* harmony import */ var _widgets_time__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widgets/time */ "./lib/widgets/time.js");
/* harmony import */ var _widgets_title__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./widgets/title */ "./lib/widgets/title.js");
/* harmony import */ var _api_project__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./api/project */ "./lib/api/project.js");







// import LogMonitorWidget from './widgets/log';



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
    console.log('JupyterLab extension ln-jupyter-extra is activating!');
    console.log('Current route:', router.current);
    console.log('Current:', router);
    // 提前处理 projectData 加载
    let projectData = {};
    try {
        const projectId = localStorage.getItem('projectId');
        projectData = await (0,_api_project__WEBPACK_IMPORTED_MODULE_3__.getProjectDetail)(projectId);
    }
    catch (error) {
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error('获取项目信息失败');
    }
    // 插件组件的实例化
    const timeWidget = new _widgets_time__WEBPACK_IMPORTED_MODULE_4__["default"]();
    timeWidget.install(app);
    // const logMonitor = new LogMonitorWidget();
    // logMonitor.install(app, statusBar);
    const sidebarWidget = new _widgets_version__WEBPACK_IMPORTED_MODULE_5__["default"]();
    sidebarWidget.install(app);
    const sidebarDataSet = new _widgets_dataset__WEBPACK_IMPORTED_MODULE_6__["default"]({ projectData });
    sidebarDataSet.install(app);
    const titleWidget = new _widgets_title__WEBPACK_IMPORTED_MODULE_7__["default"]({ projectData });
    titleWidget.install(app);
    const createVersionBtn = new _widgets_createVersion__WEBPACK_IMPORTED_MODULE_8__["default"](app);
    createVersionBtn.install(app);
    console.log('JupyterLab extension  ln-jupyter-extra activated successfully!');
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


/***/ }),

/***/ "./lib/request/baseConfig.js":
/*!***********************************!*\
  !*** ./lib/request/baseConfig.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   baseConfig: () => (/* binding */ baseConfig)
/* harmony export */ });
const domain = 'https://hero-dev.cnbita.com';
const baseConfig = {
    baseURL: domain,
    timeout: 60000 // 超时时间
};


/***/ }),

/***/ "./lib/request/index.js":
/*!******************************!*\
  !*** ./lib/request/index.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Request: () => (/* binding */ Request),
/* harmony export */   customErrorRequest: () => (/* binding */ customErrorRequest),
/* harmony export */   customNotAuthRequest: () => (/* binding */ customNotAuthRequest),
/* harmony export */   customRequest: () => (/* binding */ customRequest),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   noAllRequest: () => (/* binding */ noAllRequest),
/* harmony export */   noAuthFormatRequest: () => (/* binding */ noAuthFormatRequest),
/* harmony export */   notAuthRequest: () => (/* binding */ notAuthRequest),
/* harmony export */   otherRequest: () => (/* binding */ otherRequest)
/* harmony export */ });
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! axios */ "webpack/sharing/consume/default/axios/axios");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _baseConfig__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./baseConfig */ "./lib/request/baseConfig.js");
/* harmony import */ var _interceptor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./interceptor */ "./lib/request/interceptor.js");



/**
 * axios 封装
 * 20230217
 */
class Request {
    /**
     *
     * @param config 默认配置
     * @param flag 是否是第三方接口 默认为第三方接口 true
     */
    constructor(config, apiHookConfig) {
        const { flag = true, auth = true, skipErrorResponseInterceptor = false } = apiHookConfig;
        this.flag = flag;
        this.auth = auth;
        this.skipErrorResponseInterceptor = skipErrorResponseInterceptor;
        this.instance = axios__WEBPACK_IMPORTED_MODULE_0___default().create(config);
        this.initRequestInterceptor(this.instance);
        this.initResponseInterceptor(this.instance);
    }
    // 请求拦截器
    initRequestInterceptor(instance) {
        instance.interceptors.request.use((config) => {
            // 一般会请求拦截里面加token，用于后端的验证
            return (0,_interceptor__WEBPACK_IMPORTED_MODULE_1__.handlerRequest)(config, {
                flag: this.flag,
                auth: this.auth
            });
        }, async (err) => await Promise.reject(err));
    }
    // response拦截器
    initResponseInterceptor(instance) {
        instance.interceptors.response.use((res) => {
            // 系统如果有自定义code也可以在这里处理
            if (!this.flag) {
                return (0,_interceptor__WEBPACK_IMPORTED_MODULE_1__.handleResponse)(res);
            }
            return res;
        }, async (err) => {
            // 根据skipErrorResponseInterceptor决定是否跳过错误处理
            if (this.skipErrorResponseInterceptor) {
                return Promise.reject(err);
            }
            else {
                return await (0,_interceptor__WEBPACK_IMPORTED_MODULE_1__.handleResponseErr)(err, this.flag); // 状态码返回内容
            }
        });
    }
    // 请求方法
    async request(config) {
        return await this.instance
            .request(config)
            .then((res) => (this.flag ? res : res.data));
    }
    async get(url, config) {
        return await this.request({ method: 'get', url, ...config });
    }
    async post(url, config) {
        return await this.request({ method: 'post', url, ...config });
    }
    async put(url, config) {
        return await this.request({ method: 'put', url, ...config });
    }
    async delete(url, config) {
        return await this.request({ method: 'delete', url, ...config });
    }
}
// 默认导出Request实例
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (new Request(_baseConfig__WEBPACK_IMPORTED_MODULE_2__.baseConfig, { flag: false }));
// 自定义处理接口200时报错信息Request实例
const customRequest = new Request(_baseConfig__WEBPACK_IMPORTED_MODULE_2__.baseConfig, { flag: true });
// 自定义处理接口非200时报错信息Request实例
const customErrorRequest = new Request(_baseConfig__WEBPACK_IMPORTED_MODULE_2__.baseConfig, {
    flag: false,
    skipErrorResponseInterceptor: true
});
// 不需要token但是需要拦截器
const notAuthRequest = new Request(_baseConfig__WEBPACK_IMPORTED_MODULE_2__.baseConfig, {
    flag: false,
    auth: false
});
// 不需要token不用在意返回格式但是需要拦截器
const noAuthFormatRequest = new Request(_baseConfig__WEBPACK_IMPORTED_MODULE_2__.baseConfig, {
    flag: true,
    auth: false
});
// 不需要token不用在意返回格式不需要返回拦截器
const noAllRequest = new Request(_baseConfig__WEBPACK_IMPORTED_MODULE_2__.baseConfig, {
    flag: true,
    auth: false,
    skipErrorResponseInterceptor: true
});
// 第三方接口导出Request实例; 也可以直接引入Request类，然后传入不同的config
const otherRequest = new Request({}, {});
// 不需要token但是需要拦截器
const customNotAuthRequest = new Request(_baseConfig__WEBPACK_IMPORTED_MODULE_2__.baseConfig, {
    flag: true,
    auth: false
});


/***/ }),

/***/ "./lib/request/interceptor.js":
/*!************************************!*\
  !*** ./lib/request/interceptor.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   handleResponse: () => (/* binding */ handleResponse),
/* harmony export */   handleResponseErr: () => (/* binding */ handleResponseErr),
/* harmony export */   handlerRequest: () => (/* binding */ handlerRequest)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils */ "./lib/utils/storage.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils */ "./lib/utils/message/error.js");
// 拦截器操作


const domain = window.location.origin;
const usercenter = window.location.origin + '/heros';
(0,_utils__WEBPACK_IMPORTED_MODULE_1__.setStorage)('USREINFO', '{"token":"e4bb0a0b-b3c7-4404-8143-cf8d59464497","id":"9fedf53c3d784e74b9cf428c6825b78e","tenantId":"120273943618847469891","name":"systemuser","displayName":"systemuser","email":null,"phoneNumber":"13333333333","status":1,"description":"www","headImage":"https://hero-dev-miniogw.cnbita.com/file-open/user_avatar/7a05825ad7ef4ff99f0406860f1a984e.png","productId":"heros","lastUpdatePwdTime":null,"lastLoginTime":"2024-11-30 21:50:43","tenantFlag":1,"wechatBindFlag":1,"createTime":"2024-10-31 10:58:38","updateTime":"2024-11-05 17:32:13","createUser":"9fedf53c3d784e74b9cf428c6825b78e","updateUser":"9fedf53c3d784e74b9cf428c6825b78e","tenantInfo":{"id":"120273943618847469891","name":"systemuser","contactUserId":"9fedf53c3d784e74b9cf428c6825b78e","contactName":null,"contactMobile":null,"status":1,"companyName":"中科类脑","enterpriseState":1,"createType":1,"description":"www","productId":"heros","createTime":"2024-10-31 10:31:16","updateTime":"2024-10-31 10:10:08","createUser":"9fedf53c3d784e74b9cf428c6825b78e","updateUser":"9fedf53c3d784e74b9cf428c6825b78e","email":null},"bindFlag":1,"passwordSetType":1,"account":"systemuser"}');
(0,_utils__WEBPACK_IMPORTED_MODULE_1__.setStorage)('projectId', 'a13741493692264448241422');
// message中的错误码
// const MessageCodeDic = [
//   -3, 10133, 10117, 10119, 10121, 10122, 10124, 10134, 10157, 10307, 10315,
//   61000
// ];
// message中的错误码
const MessageCodeDic = [1027];
// 处理请求头，一般比如在header加token
const handlerRequest = (config, apiHookConfig) => {
    if (!apiHookConfig.auth) {
        return config;
    }
    const USREINFO = JSON.parse((0,_utils__WEBPACK_IMPORTED_MODULE_1__.getStorage)('USREINFO') || '{}') || {};
    // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
    if (USREINFO.token) {
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        config.headers.token = USREINFO.token;
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        config.headers['X-Agent-Token'] =
            'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidG9rZW5fdHlwZSI6ImFjY2Vzc190b2tlbiIsImlhdCI6MTY3MzIzMTUzNiwiaXNzIjoia3ViZXNwaGVyZSIsIm5iZiI6MTY3MzIzMTUzNn0.7O9n5M-qzJPgl2gILJ8hXNuwDPlrxdrl8CEDMLCfTyQ';
    }
    else {
        window.location.replace(usercenter + '/login?redirect=' + window.location.origin);
    }
    return config;
};
// 根据情况处理返回数据
const handleResponse = (res) => {
    // 如果后端返回的是code为0，则直接返回.data.data；如果不为0，则把massage也返回出去
    // todo 在某些情况下instance可能会有用处
    const { data } = res;
    const { code, message } = data.message;
    // 正常状态返回
    if (code === 0) {
        return data;
    }
    // 异常状态返回 根据不同的code判断接下来的操作
    switch (true) {
        // 未登录
        case MessageCodeDic.includes(code):
            window.location.replace(usercenter + '/login?redirect=' + domain);
            break;
        case code === 401:
            // 未授权
            // noAuthError(JSON.parse(getStorage('USREINFO') || '{}') || {});
            if (message) {
                void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.error(message);
            }
            break;
        case code !== 0:
            if (message) {
                void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.error(message);
            }
    }
    return Promise.reject(res);
};
const handleResponseErr = async (error, flag = false) => {
    const { response, request } = error;
    if (response !== null) {
        // 当响应状态码为非2xx时，可以在这里进行错误处理
        // console.log(response.status);
        // console.log(response.data);
        // console.log(response.headers);
        // 判断http状态码非2xx时 是否存在业务代码的code
        //                     存在code 匹配全局message 匹配不上 判断是否有message
        //                                                          有：提示message
        //                                                          否：根据http状态码提示
        const { data: { message } } = response;
        if (!flag) {
            const { code = undefined, message = undefined } = (response === null || response === void 0 ? void 0 : response.data)
                ? response.data.message || {}
                : {};
            // 登录过期 需要重新登录
            if (MessageCodeDic.includes(code)) {
                window.location.replace(usercenter + '/login?redirect=' + domain);
            }
            else if ((response === null || response === void 0 ? void 0 : response.status) === 401 && code === 401) {
                // 未授权
                if (message) {
                    void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.error(message);
                }
                // noAuthError(JSON.parse(getStorage('USREINFO') || '{}') || {});
            }
            else if (code !== 0) {
                // 现在的逻辑是 返回的数据code不是0 http状态码可能也不是0 所以需要在这里进行拦截
                if (message) {
                    void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.error(message);
                }
            }
            else {
                void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.error((0,_utils__WEBPACK_IMPORTED_MODULE_2__.MessageCodeError)(message, (0,_utils__WEBPACK_IMPORTED_MODULE_2__.MessageCodeError)({ code: response === null || response === void 0 ? void 0 : response.status })));
            }
        }
        if (message === null || message === void 0 ? void 0 : message.code) {
            // 异常状态返回 根据不同的code判断接下来的操作
            switch (true) {
                // 未登录
                case MessageCodeDic.includes(message === null || message === void 0 ? void 0 : message.code):
                    window.location.replace(usercenter + '/login?redirect=' + domain);
                    break;
            }
        }
        // if (data) {
        //   return (await Promise.reject(data)) as any;
        // }
    }
    else if (error.code === 'ECONNABORTED' &&
        error.message.includes('timeout')) {
        // 超时处理
        void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.warning('请求超时，请检查网络连接并重新尝试！');
    }
    else if (request !== null) {
        // 当没有响应时，可以在这里进行错误处理：个人建议无需处理
        void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.error((0,_utils__WEBPACK_IMPORTED_MODULE_2__.MessageCodeError)({}));
    }
    else {
        // 其他错误，可以在这里进行错误处理
        void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.error((0,_utils__WEBPACK_IMPORTED_MODULE_2__.MessageCodeError)({}));
        console.log('Error', error.message);
    }
    // 超时判断
    return await Promise.reject(error);
};


/***/ }),

/***/ "./lib/utils/message/error.js":
/*!************************************!*\
  !*** ./lib/utils/message/error.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MessageCodeError: () => (/* binding */ MessageCodeError),
/* harmony export */   codeDic: () => (/* binding */ codeDic)
/* harmony export */ });
// 错误码对应字典值 code => message
// 注：涉及具体业务的code不要放到这里 例如：code为1001 在A业务中提示的是参数不能为空
//                                               在B业务中提示的是删除失败...
const codeDic = {
    1001: '参数不能为空',
    1002: '参数不能为null',
    1003: '参数类型错误',
    1004: '空指针错误',
    1005: '参数验证失败',
    1020: '不支持表情符号',
    1021: '用户名错误',
    1022: '帐号错误',
    1023: '密码错误',
    1024: '用户名或密码错误',
    1025: '帐号或密码错误',
    1026: '验证码错误',
    1200: '资源操作错误',
    1201: '资源添加错误',
    1202: '资源删除错误',
    1203: '资源更新错误',
    1204: '资源查询错误',
    1205: '资源查询数据为空',
    1206: '不允许重复资源',
    1300: '文件操作错误',
    1301: '文件未找到',
    1302: '文件访问被拒绝',
    1303: '文件读取失败',
    1304: '文件写入失败',
    1305: '文件创建失败',
    1306: '文件删除失败',
    1307: '文件复制错误',
    1308: '文件移动失败',
    1309: '文件目录未找到',
    1310: '文件目录拒绝访问',
    1311: '文件目录读取失败',
    1312: '文件目录写入失败',
    1400: '请求第三方组件失败',
    1401: '请求第三方组件超时',
    1402: '第三方组件响应错误',
    1403: '请求内部组件错误',
    1404: '请求内部组件超时',
    1405: '内部组件响应错误',
    400: '请求失败',
    401: '未经授权',
    403: '被禁止的',
    404: '请求不存在',
    405: '不允许此请求方法',
    500: '内部服务器错误',
    502: '网关错误',
    503: '服务不可用',
    504: '网关超时'
};
/**
 *
 * @param data 服务端返回数据结构 {code: 0, message: 'message'}
 * @returns error message
 * @description 判断code是否为number 是：优先匹配code 在字典中对应的提示文字 其次提示data.message 最后提示defaultMsg
 *                                  否：提示defaultMsg
 */
const MessageCodeError = (data, defaultMsg = '系统异常，请联系管理员！') => {
    var _a;
    return typeof data.code === 'number'
        ? (_a = (codeDic[data.code] || data.message)) !== null && _a !== void 0 ? _a : defaultMsg
        : defaultMsg;
    // return (codeDic[data.code] || data.message) ?? defaultMsg
};


/***/ }),

/***/ "./lib/utils/storage.js":
/*!******************************!*\
  !*** ./lib/utils/storage.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   clearStorage: () => (/* binding */ clearStorage),
/* harmony export */   getStorage: () => (/* binding */ getStorage),
/* harmony export */   removeStorage: () => (/* binding */ removeStorage),
/* harmony export */   setStorage: () => (/* binding */ setStorage)
/* harmony export */ });
// Web storage API
// localStorage用的较多，所以在创建和获取的时候默认为storage，如果是用sessionStorage请传另一个参数flag为false
const getStorage = (key, flag = true) => {
    return flag ? localStorage.getItem(key) : sessionStorage.getItem(key);
};
const setStorage = (key, value, flag = true) => {
    flag ? localStorage.setItem(key, value) : sessionStorage.setItem(key, value);
};
const removeStorage = (key, flag = true) => {
    flag ? localStorage.removeItem(key) : sessionStorage.removeItem(key);
};
const clearStorage = (flag = true) => {
    flag ? localStorage.clear() : sessionStorage.clear();
};


/***/ }),

/***/ "./lib/widgets/createVersion.js":
/*!**************************************!*\
  !*** ./lib/widgets/createVersion.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react_dom_client__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-dom/client */ "./node_modules/react-dom/client.js");
/* harmony import */ var _api_project__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api/project */ "./lib/api/project.js");





// 版本创建表单组件
const VersionCreationForm = ({ onClose, onSubmit }) => {
    const [formData, setFormData] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)({
        name: '',
        description: ''
    });
    const [errors, setErrors] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)({
        name: '',
        description: ''
    });
    // 校验版本名称
    const validateName = (name) => {
        const nameRegex = /^[a-zA-Z0-9.]+$/;
        if (!name) {
            return '版本名称不能为空';
        }
        if (name.length > 10) {
            return '版本名称长度不能超过10个字符';
        }
        if (!nameRegex.test(name)) {
            return '版本名称只能包含英文、数字和.';
        }
        return '';
    };
    // 校验描述
    const validateDescription = (description) => {
        if (description.length > 300) {
            return '版本描述不能超过300个字符';
        }
        return '';
    };
    // 处理输入变化
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };
    // 提交表单
    const handleSubmit = async () => {
        const nameError = validateName(formData.name);
        const descriptionError = validateDescription(formData.description);
        // 设置错误信息
        setErrors({
            name: nameError,
            description: descriptionError
        });
        // 如果有错误，阻止提交
        if (nameError || descriptionError) {
            return;
        }
        try {
            // 调用提交接口
            await onSubmit({
                name: formData.name,
                description: formData.description
            });
            // 成功后关闭弹框
            onClose();
        }
        catch (error) {
            console.error('提交失败', error);
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { style: {
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000
        } },
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { style: {
                backgroundColor: 'white',
                padding: '20px',
                borderRadius: '8px',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                width: '500px'
            } },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h2", { style: { marginTop: 0, marginBottom: '20px' } }, "\u521B\u5EFA\u7248\u672C"),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { style: { marginBottom: '15px' } },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("label", { style: {
                        display: 'block',
                        marginBottom: '5px',
                        fontWeight: 'bold'
                    } }, "\u7248\u672C\u540D\u79F0"),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("input", { type: "text", name: "name", value: formData.name, onChange: handleChange, placeholder: "\u8BF7\u8F93\u5165\u7248\u672C\u540D\u79F0\uFF08\u82F1\u6587+\u6570\u5B57+.\uFF0C\u6700\u957F10\u5B57\u7B26\uFF09", style: {
                        width: '100%',
                        padding: '8px',
                        boxSizing: 'border-box',
                        borderColor: errors.name ? 'red' : '#ccc',
                        borderWidth: '1px',
                        borderStyle: 'solid'
                    } }),
                errors.name && (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { style: { color: 'red', margin: '5px 0 0' } }, errors.name))),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("label", { style: {
                        display: 'block',
                        marginBottom: '5px',
                        fontWeight: 'bold'
                    } }, "\u7248\u672C\u63CF\u8FF0"),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("textarea", { name: "description", value: formData.description, onChange: handleChange, placeholder: "\u8BF7\u8F93\u5165\u7248\u672C\u63CF\u8FF0\uFF08\u6700\u957F300\u5B57\u7B26\uFF09", style: {
                        width: '100%',
                        padding: '8px',
                        boxSizing: 'border-box',
                        minHeight: '100px',
                        borderColor: errors.description ? 'red' : '#ccc',
                        borderWidth: '1px',
                        borderStyle: 'solid'
                    } }),
                errors.description && (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { style: { color: 'red', margin: '5px 0 0' } }, errors.description))),
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { style: {
                    display: 'flex',
                    justifyContent: 'flex-end',
                    marginTop: '20px'
                } },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("button", { onClick: onClose, style: {
                        padding: '8px 16px',
                        marginRight: '10px',
                        backgroundColor: '#f0f0f0',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                    } }, "\u53D6\u6D88"),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("button", { onClick: handleSubmit, style: {
                        padding: '8px 16px',
                        backgroundColor: '#4CAF50',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                    } }, "\u786E\u5B9A")))));
};
class SaveButton extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton {
    constructor(app) {
        const COMMAND_ID = 'version:create';
        app.commands.addCommand(COMMAND_ID, {
            label: '生成版本',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.saveIcon,
            execute: () => {
                this.handleSave(app);
            }
        });
        super({
            commands: app.commands,
            id: COMMAND_ID
        });
        this.dialogContainer = null;
        this.dialogRoot = null;
        this.id = 'version-list-save-button';
        this._app = app;
    }
    install(app) {
        app.shell.add(this, 'top', {
            rank: 1000
        });
    }
    handleSave(app) {
        // 创建对话框容器
        this.dialogContainer = document.createElement('div');
        document.body.appendChild(this.dialogContainer);
        // 创建 React 根
        this.dialogRoot = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_3__.createRoot)(this.dialogContainer);
        const closeDialog = () => {
            if (this.dialogRoot && this.dialogContainer) {
                this.dialogRoot.unmount();
                document.body.removeChild(this.dialogContainer);
                this.dialogContainer = null;
                this.dialogRoot = null;
            }
        };
        const submitVersion = async (data) => {
            try {
                await (0,_api_project__WEBPACK_IMPORTED_MODULE_4__.addProjectVersion)({
                    projectId: localStorage.getItem('projectId') || '',
                    version: data.name,
                    description: data.description
                });
                this.refreshData(this._app);
            }
            catch (error) {
                console.error('版本创建失败:', error);
                alert('版本创建失败，请重试');
            }
        };
        // 渲染对话框
        this.dialogRoot.render(react__WEBPACK_IMPORTED_MODULE_2___default().createElement(VersionCreationForm, { onClose: closeDialog, onSubmit: submitVersion }));
    }
    refreshData(app) {
        const widgets = Array.from(app.shell.widgets('left'));
        console.log(widgets);
        const versionListWidget = widgets.find(widget => widget.id === 'ln-version-list-sidebar');
        console.log(versionListWidget);
        if (versionListWidget) {
            // 直接调用 getVersions 方法刷新列表
            versionListWidget.getVersions();
        }
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SaveButton);


/***/ }),

/***/ "./lib/widgets/dataset.js":
/*!********************************!*\
  !*** ./lib/widgets/dataset.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _api_project__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api/project */ "./lib/api/project.js");
/* harmony import */ var _components_DatasetListPanel__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/DatasetListPanel */ "./lib/components/DatasetListPanel.js");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);






class DataSetListSidebarWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(options) {
        super();
        this.addClass('ln-dataset-list-sidebar'); // 使用 ln- 前缀
        this.id = 'ln-dataset-list-dataset';
        this.title.caption = '数据集';
        this.title.label = '数据集';
        this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.tableRowsIcon;
        this.title.closable = true; // 允许关闭
        this.projectData = options.projectData || {};
        this.datasetList = options.projectData.storageList || [];
        this.listContainer = document.createElement('div');
        this.listContainer.className = 'ln-dataset-list';
        this.node.appendChild(this.listContainer);
        this.params = {
            searchKey: '',
            pageSize: 15,
            pageNum: 1,
            tagLabels: [],
            sortType: 'deployTime'
        };
        // 调用获取版本的函数
        this.getVersions();
    }
    async getToken(id) {
        try {
            this.token = await (0,_api_project__WEBPACK_IMPORTED_MODULE_4__.getFileProxyToken)({
                expires: 3600,
                businessId: id,
                businessType: 1
            });
        }
        catch (error) {
            console.error('Error in getToken:', error);
            throw error;
        }
    }
    async queryFileList(dataset, token) {
        var _a;
        const queryParams = {
            bucketName: dataset.bucketCrName,
            storageType: 'filesystem',
            dir: dataset.bucketPath.slice(1) + '/',
            pageNumber: 1,
            pageSize: 2147483647
        };
        try {
            if (!token) {
                throw new Error('No valid auth token');
            }
            const res = await (0,_api_project__WEBPACK_IMPORTED_MODULE_4__.getFileList)(queryParams, token, dataset.clusterId);
            if ((_a = res.data) === null || _a === void 0 ? void 0 : _a.data.fileList) {
                dataset.fileList = res.data.data.fileList;
            }
            else {
                console.warn('File list is empty or undefined');
                dataset.fileList = [];
            }
        }
        catch (error) {
            console.error('Error in getFileListData:', error);
            throw error;
        }
    }
    async getVersions() {
        try {
            await Promise.all(this.datasetList.map(async (item) => {
                await this.getToken(item.businessId);
                await this.queryFileList(item, this.token);
                console.log(this.datasetList);
            }));
            this.updateDatasetList(this.datasetList);
        }
        catch (error) {
            console.error('请求数据时出错:', error);
            throw error; // 重新抛出错误
        }
    }
    updateDatasetList(data) {
        react_dom__WEBPACK_IMPORTED_MODULE_2___default().render(react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", null, data.map((dataset, index) => (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_components_DatasetListPanel__WEBPACK_IMPORTED_MODULE_5__["default"], { key: `${dataset.name}-${index}`, title: dataset.name, files: dataset.fileList || [], onFileClick: fileName => {
                console.log(`Clicked file: ${fileName}`);
            } })))), this.listContainer);
    }
    install(app) {
        app.shell.add(this, 'left', {
            rank: 900,
            type: 'tab'
        });
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DataSetListSidebarWidget);


/***/ }),

/***/ "./lib/widgets/time.js":
/*!*****************************!*\
  !*** ./lib/widgets/time.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

class UsageTimeWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.id = 'usage-time-widget';
        this.title.label = '使用时间';
        this.title.closable = true;
        this.addClass('usage-time-widget');
        this.startTime = Date.now(); // 记录启动时间
        this.updateUsageTime();
        setInterval(() => this.updateUsageTime(), 1000); // 每秒更新
    }
    updateUsageTime() {
        const elapsedTime = Math.floor((Date.now() - this.startTime) / 1000); // 计算已用时间（秒）
        const hours = Math.floor(elapsedTime / 3600);
        const minutes = Math.floor((elapsedTime % 3600) / 60);
        const seconds = elapsedTime % 60;
        this.node.style.cssText = 'margin-top:5px';
        this.node.innerText = `已使用时间: ${hours}小时 ${minutes}分钟 ${seconds}秒`;
    }
    install(app) {
        app.shell.add(this, 'top', {
            rank: 998
        });
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (UsageTimeWidget);


/***/ }),

/***/ "./lib/widgets/title.js":
/*!******************************!*\
  !*** ./lib/widgets/title.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

class TitleWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(options) {
        super();
        this.nodeTitle = document.createElement('div');
        this.nodeTitle.textContent = options.projectData.name || '';
        this.nodeTitle.style.cssText = 'margin-left:350px;margin-top:5px';
        this.widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget({ node: this.nodeTitle });
        this.widget.id = 'jupyter-title';
    }
    install(app) {
        app.shell.add(this.widget, 'top', { rank: 501 });
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (TitleWidget);


/***/ }),

/***/ "./lib/widgets/version.js":
/*!********************************!*\
  !*** ./lib/widgets/version.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _api_project__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api/project */ "./lib/api/project.js");
/* harmony import */ var react_dom_client__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dom/client */ "./node_modules/react-dom/client.js");
/* harmony import */ var _components_VersionList__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/VersionList */ "./lib/components/VersionList.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);






class VersionListSidebarWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.addClass('ln-version-list-sidebar'); // 使用 ln- 前缀
        this.id = 'ln-version-list-sidebar';
        this.title.caption = '版本';
        this.title.label = '版本';
        this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.listIcon;
        this.title.closable = true; // 允许关闭
        // 创建列表容器
        this.listContainer = document.createElement('div');
        this.listContainer.className = 'ln-version-list';
        this.node.appendChild(this.listContainer);
        this.params = {
            searchKey: '',
            pageSize: 15,
            pageNum: 1,
            tagLabels: [],
            sortType: 'deployTime'
        };
        // 调用获取版本的函数
        this.getVersions();
    }
    async getVersions() {
        const params = {
            projectId: localStorage.getItem('projectId') || '',
            pageSize: 100,
            pageNum: 1
        };
        try {
            const res = await (0,_api_project__WEBPACK_IMPORTED_MODULE_4__.getProjectVersionList)(params);
            const list = res.list;
            this.updateVersionList(list); // 更新版本列表
        }
        catch (error) {
            console.error('Failed to fetch versions:', error);
        }
    }
    updateVersionList(data) {
        this.listContainer.innerHTML = '';
        const versions = data || [];
        // 确保正确处理空数组情况
        if (versions.length === 0) {
            this.listContainer.innerHTML = '<div>暂无版本</div>';
            return;
        }
        // 使用 createRoot 替代 ReactDOM.render（推荐）
        const root = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_2__.createRoot)(this.listContainer);
        root.render(react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", null, versions.map(version => (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_components_VersionList__WEBPACK_IMPORTED_MODULE_5__.VersionList, { key: version.version, version: version.version, createTime: version.createTime })))));
    }
    install(app) {
        app.shell.add(this, 'left', {
            rank: 900,
            type: 'tab'
        });
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (VersionListSidebarWidget);


/***/ }),

/***/ "./node_modules/react-dom/client.js":
/*!******************************************!*\
  !*** ./node_modules/react-dom/client.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {



var m = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
if (false) {} else {
  var i = m.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
  exports.createRoot = function(c, o) {
    i.usingClientEntryPoint = true;
    try {
      return m.createRoot(c, o);
    } finally {
      i.usingClientEntryPoint = false;
    }
  };
  exports.hydrateRoot = function(c, h, o) {
    i.usingClientEntryPoint = true;
    try {
      return m.hydrateRoot(c, h, o);
    } finally {
      i.usingClientEntryPoint = false;
    }
  };
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.f9cd64e0db3902f37cf3.js.map