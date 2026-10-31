'use strict';
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  // Open native folder-picker dialog; resolves to array of selected paths
  openFolder: () => ipcRenderer.invoke('open-folder'),

  // Listen for global media key events forwarded from the main process
  onMediaKey: (cb) => {
    const handler = (_event, key) => cb(key);
    ipcRenderer.on('media-key', handler);
    return () => ipcRenderer.removeListener('media-key', handler);
  },

  platform: process.platform,
});
