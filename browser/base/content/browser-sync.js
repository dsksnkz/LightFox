/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var gSync = {
  FXA_ENABLED: false,
  isSignedIn: false,
  sendTabConfiguredAndLoading: false,
  _isCurrentlySyncing: false,

  init() {
    document.documentElement.setAttribute("fxadisabled", true);
    document.documentElement.setAttribute("fxastatus", "not_configured");
    for (const item of document.querySelectorAll(".sync-ui-item")) {
      item.hidden = true;
    }
  },
  uninit() {},
  maybeUpdateUIState() {},
  emitFxaToolbarTelemetry() {},
  getSyncPromoState: () => null,
  handleSyncPromoAction() {},
  toggleAccountPanel() {},
  openPrefs() {},
  openConnectAnotherDevice() {},
  openSignInAgainPage() {},
  openDevicesManagementPage() {},
  openSyncedTabsPanel() {},
  openSendTabHelp() {},
  openPairDevice() {},
  openFxAEmailFirstPage() {},
  doSync() {},
  disconnect: async () => false,
  formatLastSyncDate: () => null,
  refreshSyncButtonsTooltip() {},
  ensureFxaDevices: async () => {},
  getSendTabTargets: () => [],
  getTargetClientType: () => "",
  populateSendTabToDevicesMenu() {},
  populateSendTabToolbarButton() {},
  sendTabToolbarButtonShouldBeEnabled: () => false,
  sendTabsAndConfirm: async () => {},
  updateTabContextMenu() {},
  updateContentContextMenu() {},
  _resetSendTabExposureTracking() {},
};
