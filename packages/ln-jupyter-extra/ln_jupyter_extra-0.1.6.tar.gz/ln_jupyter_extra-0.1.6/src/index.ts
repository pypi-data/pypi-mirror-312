import {
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { IStatusBar } from '@jupyterlab/statusbar';
import createVersion from './widgets/createVersion';
import VersionListSidebarWidget from './widgets/version';
import DataSetListSidebarWidget from './widgets/dataset';
import UsageTimeWidget from './widgets/time';
import LogMonitorWidget from './widgets/log';
import TitleWidget from './widgets/title';
import { getProjectDetail } from './api/project';
import { Notification } from '@jupyterlab/apputils';
import VariableInspectorPlugins from './widgets/variable/index';
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

async function activate(
  app: JupyterFrontEnd,
  palette: ICommandPalette,
  restorer: ILayoutRestorer | null,
  statusBar: IStatusBar
): Promise<void> {
  console.log('JupyterLab extension ln-jupyter-extra is activating!');

  // 提前处理 projectData 加载
  let projectData: any = {};
  try {
    const projectId = localStorage.getItem('projectId');
    projectData = await getProjectDetail(projectId);
  } catch (error) {
    Notification.error('获取项目信息失败');
  }

  // 插件组件的实例化
  const timeWidget = new UsageTimeWidget();
  timeWidget.install(app);

  const logMonitor = new LogMonitorWidget();
  logMonitor.install(app, statusBar);

  const sidebarWidget = new VersionListSidebarWidget();
  sidebarWidget.install(app);

  const sidebarDataSet = new DataSetListSidebarWidget({ projectData });
  sidebarDataSet.install(app);

  const titleWidget = new TitleWidget({ projectData });
  titleWidget.install(app);

  const createVersionBtn = new createVersion(app);
  createVersionBtn.install(app);

  console.log('JupyterLab extension  ln-jupyter-extra activated successfully!');
}

const lnPlugin: JupyterFrontEndPlugin<void> = {
  id: 'ln-notebook:plugin',
  description: 'leinao extra jupyter plugin',
  autoStart: true,
  requires: [ICommandPalette, ILayoutRestorer],
  optional: [IStatusBar],
  activate: activate
};

const plugins = [lnPlugin, ...VariableInspectorPlugins];
export default plugins;
