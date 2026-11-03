/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

export const Weave = {
  Service: { isLoggedIn: false, scheduler: { autoConnect() {} } },
  Status: { checkSetup: () => "service.client_not_configured" },
  Svc: {
    Obs: { add() {}, remove() {} },
    PrefBranch: { getCharPref: (_name, fallback) => fallback },
  },
};
