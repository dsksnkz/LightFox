/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const no = () => false;
const noop = () => {};

export const LinkPreview = {
  canShowKeyPoints: false,
  canShowPreferences: false,
  shouldShowContextMenu: no,
  handleContextMenuClick: noop,
  init: noop,
  teardown: noop,
};
