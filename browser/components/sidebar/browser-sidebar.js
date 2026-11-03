/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var SidebarController = {
  currentID: "",
  lastOpenedId: null,
  isOpen: false,
  initialized: false,
  browser: null,
  sidebarMain: null,
  sidebarContainer: null,
  sidebarRevampVisibility: "hide-sidebar",
  _positionStart: true,
  _state: null,
  _permissions: { updateFromBrowserState() {} },
  promiseInitialized: Promise.resolve(),
  expandOnHoverComplete: Promise.resolve(),

  show(id) {
    if (id == "viewBookmarksSidebar") {
      PlacesCommandHook.showPlacesOrganizer("AllBookmarks");
    } else if (id == "viewHistorySidebar") {
      PlacesCommandHook.showPlacesOrganizer("History");
    }
    return Promise.resolve();
  },
  _show(id) {
    return this.show(id);
  },
  toggle(id) {
    return this.show(id);
  },
  hide() {},
  handleToolbarButtonClick() {},
  updateUIState() {},
  getUIState() {
    return null;
  },
  markSessionRestoreStateReceived() {},
  updateToolbarButton() {},
  updateShortcut() {},
  updatePinnedTabsHeightOnResize() {},
  toggleVerticalTabs() {},
  setPosition() {},
  reversePosition() {},
  registerExtension() {},
  removeExtension() {},
  setExtensionAttributes() {},
};
