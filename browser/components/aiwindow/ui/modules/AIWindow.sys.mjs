/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

export const AIWINDOW_URL = "about:blank";

const no = () => false;
const noop = () => {};

export const AIWindow = {
  initialStartupURL: null,
  newTabURL: null,
  isDefaultWindow: false,
  appMenu: noop,
  isOpeningAIWindow: no,
  isEnabled: false,
  isBlocked: true,
  chatStore: null,
  isAIWindowEnabled: no,
  isAIWindowActive: no,
  isAIWindowActiveAndEnabled: no,
  isAIWindowNewTabPage: no,
  isAIWindowContentPage: no,
  shouldOpenAsSmartWindow: no,
  shouldUseImmersiveView: no,
  hasActiveAIWindows: no,
  hasActiveChatInBrowser: no,
  handleAIWindowOptions: no,
  init: noop,
  uninit: noop,
  launchWindow: noop,
  toggleAIWindow: noop,
  createAITab: noop,
  updateImmersiveView: noop,
  recordOpenWindowTelemetry: noop,
  getChatTabConversationId: () => null,
  getSmartbarForWindow: () => null,
};
