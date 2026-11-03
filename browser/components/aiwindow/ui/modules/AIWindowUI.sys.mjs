/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const no = () => false;
const noop = () => {};

export const AIWindowUI = {
  BOX_ID: "ai-window-box",
  BROWSER_ID: "ai-window-browser",
  isSidebarOpen: no,
  openSidebar: noop,
  closeSidebar: noop,
  toggleSidebar: noop,
  toggleGroupTabsPanel: noop,
  toggleMonitorPanel: noop,
  showMonitorCreateForm: noop,
};
