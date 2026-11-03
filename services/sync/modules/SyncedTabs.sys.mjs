/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

export const SyncedTabs = {
  TOPIC_TABS_CHANGED: "services.sync.tabs.changed",
  hasSyncedThisSession: false,
  isConfiguredToSyncTabs: false,
  getTabClients: async () => [],
  getRecentTabs: async () => [],
  sortTabClientsByLastUsed() {},
  syncTabs: async () => false,
  recordSyncedTabsTelemetry() {},
};
