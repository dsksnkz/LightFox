/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const noop = () => {};

export const GenAI = {
  chatProviders: new Map(),
  currentChatProviderInfo: null,
  canOfferChatbot: false,
  init: noop,
  initializeSelectionShortcutPanel: noop,
  buildAskChatMenu: noop,
  buildTabMenu: noop,
  buildTabSummarizeItem: noop,
  summarizeCurrentPage: noop,
};
