/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const STATE = Object.freeze({ status: "not_configured", syncing: false });

export const UIState = {
  ON_UPDATE: "sync-ui-state:update",
  STATUS_LOGIN_FAILED: "login_failed",
  STATUS_NOT_CONFIGURED: "not_configured",
  STATUS_NOT_VERIFIED: "not_verified",
  STATUS_SIGNED_IN: "signed_in",
  isReady: () => true,
  get: () => STATE,
  refresh() {},
};
