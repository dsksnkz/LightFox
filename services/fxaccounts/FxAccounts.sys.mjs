/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const device = {
  recentDeviceList: [],
  getLocalName: () => "",
  refreshDeviceList: async () => {},
};

export class FxAccounts {
  static config = {
    isProductionConfig: () => false,
    promiseConnectAccountURI: async () => "about:blank",
    promiseManageURI: async () => "about:blank",
  };
  device = device;
  getSignedInUser = async () => null;
  hasLocalSession = async () => false;
  listAttachedOAuthClients = async () => [];
  getOAuthToken = async () => null;
  removeCachedOAuthToken = async () => {};
}

const singleton = new FxAccounts();

export function getFxAccountsSingleton() {
  return singleton;
}
