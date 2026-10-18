import { app, BrowserWindow, ipcMain, dialog, globalShortcut, shell, Menu } from 'electron';
import { fileURLToPath } from 'url';
import path from 'path';
import { startServer } from './server.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

let mainWindow;
let serverPort;

// ── Single instance lock ──────────────────────────────────────────────────────
const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
  process.exit(0);
}
app.on('second-instance', () => {
  if (mainWindow) {
    if (mainWindow.isMinimized()) mainWindow.restore();
    mainWindow.focus();
  }
});

// ── App menu (minimal) ────────────────────────────────────────────────────────
function buildMenu() {
  const template = [
    {
      label: 'Mediabox',
      submenu: [
        { label: 'About Mediabox', role: 'about' },
        { type: 'separator' },
        { label: 'Quit', accelerator: 'CmdOrCtrl+Q', click: () => app.quit() },
      ],
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'cut' }, { role: 'copy' }, { role: 'paste' }, { role: 'selectAll' },
      ],
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' },
        ...(process.env.NODE_ENV === 'development'
          ? [{ type: 'separator' }, { role: 'toggleDevTools' }]
          : []),
      ],
    },
    {
      label: 'Window',
      submenu: [
        { role: 'minimize' },
        { role: 'zoom' },
        { role: 'close' },
      ],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

// ── Create window ─────────────────────────────────────────────────────────────
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    backgroundColor: '#0F0F23',
    show: false,
    title: 'Mediabox',
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });

  mainWindow.loadURL(`http://127.0.0.1:${serverPort}`);

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Open external links in the real browser, not Electron
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

// ── IPC handlers ──────────────────────────────────────────────────────────────
function registerIPC() {
  // Native folder picker — returns array of chosen paths (empty if cancelled)
  ipcMain.handle('open-folder', async () => {
    if (!mainWindow) return [];
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ['openDirectory', 'multiSelections'],
      title: 'Add Music / Video Folder',
    });
    return result.canceled ? [] : result.filePaths;
  });
}

// ── Global media keys ─────────────────────────────────────────────────────────
function registerMediaKeys() {
  const send = (ch) => mainWindow?.webContents.send('media-key', ch);
  globalShortcut.register('MediaPlayPause',      () => send('playpause'));
  globalShortcut.register('MediaNextTrack',      () => send('next'));
  globalShortcut.register('MediaPreviousTrack',  () => send('prev'));
}

// ── Boot sequence ─────────────────────────────────────────────────────────────
app.whenReady().then(async () => {
  try {
    serverPort = await startServer(0); // 0 = OS picks a free port
  } catch (err) {
    console.error('Failed to start server:', err);
    app.quit();
    return;
  }

  buildMenu();
  registerIPC();
  createWindow();
  registerMediaKeys();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});
