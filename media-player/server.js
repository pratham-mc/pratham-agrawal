import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { parseFile } from 'music-metadata';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = process.env.PORT || 3000;
const CONFIG_FILE    = path.join(__dirname, 'config.json');
const PLAYLISTS_FILE = path.join(__dirname, 'playlists.json');

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const encodeId = (p) => Buffer.from(p).toString('base64url');
const decodeId = (id) => Buffer.from(id, 'base64url').toString();

const AUDIO_EXT = new Set(['.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac', '.wma', '.opus']);
const VIDEO_EXT = new Set(['.mp4', '.mkv', '.avi', '.mov', '.webm', '.m4v', '.wmv', '.flv']);

const MIME = {
  '.mp3': 'audio/mpeg', '.flac': 'audio/flac', '.wav': 'audio/wav',
  '.ogg': 'audio/ogg', '.m4a': 'audio/mp4', '.aac': 'audio/aac',
  '.opus': 'audio/ogg', '.wma': 'audio/x-ms-wma',
  '.mp4': 'video/mp4', '.mkv': 'video/x-matroska', '.avi': 'video/x-msvideo',
  '.mov': 'video/quicktime', '.webm': 'video/webm', '.m4v': 'video/mp4',
  '.wmv': 'video/x-ms-wmv', '.flv': 'video/x-flv',
};

function scanDir(dirPath, results = []) {
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    for (const e of entries) {
      if (e.name.startsWith('.')) continue;
      const full = path.join(dirPath, e.name);
      if (e.isDirectory()) {
        scanDir(full, results);
      } else {
        const ext = path.extname(e.name).toLowerCase();
        if (AUDIO_EXT.has(ext) || VIDEO_EXT.has(ext)) {
          const st = fs.statSync(full);
          results.push({
            id: encodeId(full),
            name: e.name,
            path: full,
            ext,
            type: AUDIO_EXT.has(ext) ? 'audio' : 'video',
            size: st.size,
            modified: st.mtimeMs,
          });
        }
      }
    }
  } catch (_) {}
  return results;
}

app.get('/api/config', (req, res) => {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      res.json(JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')));
    } else {
      res.json({ directories: [] });
    }
  } catch (_) {
    res.json({ directories: [] });
  }
});

app.post('/api/config', (req, res) => {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify({ directories: req.body.directories || [] }, null, 2));
  res.json({ ok: true });
});

app.get('/api/playlists', (req, res) => {
  try {
    if (fs.existsSync(PLAYLISTS_FILE)) {
      res.json(JSON.parse(fs.readFileSync(PLAYLISTS_FILE, 'utf8')));
    } else {
      res.json({ playlists: [] });
    }
  } catch (_) {
    res.json({ playlists: [] });
  }
});

app.post('/api/playlists', (req, res) => {
  fs.writeFileSync(PLAYLISTS_FILE, JSON.stringify({ playlists: req.body.playlists || [] }, null, 2));
  res.json({ ok: true });
});

app.post('/api/scan', (req, res) => {
  const dirs = req.body.directories || [];
  const files = [];
  for (const d of dirs) {
    if (fs.existsSync(d)) scanDir(d, files);
  }
  res.json({ files });
});

app.get('/api/metadata/:id', async (req, res) => {
  const fp = decodeId(req.params.id);
  try {
    const meta = await parseFile(fp, { skipCovers: false, duration: true });
    const c = meta.common;
    res.json({
      title: c.title || null,
      artist: c.artist || c.albumartist || null,
      album: c.album || null,
      year: c.year || null,
      genre: c.genre?.[0] || null,
      duration: meta.format.duration || null,
      hasArtwork: !!(c.picture && c.picture.length > 0),
    });
  } catch (_) {
    res.json({ title: null, artist: null, album: null, duration: null, hasArtwork: false });
  }
});

app.get('/api/artwork/:id', async (req, res) => {
  const fp = decodeId(req.params.id);
  try {
    const meta = await parseFile(fp, { skipCovers: false });
    const pic = meta.common.picture?.[0];
    if (!pic) return res.status(404).end();
    res.set('Content-Type', pic.format || 'image/jpeg');
    res.set('Cache-Control', 'public, max-age=86400');
    res.send(Buffer.from(pic.data));
  } catch (_) {
    res.status(404).end();
  }
});

app.get('/stream/:id', (req, res) => {
  const fp = decodeId(req.params.id);
  if (!fs.existsSync(fp)) return res.status(404).end();

  const stat = fs.statSync(fp);
  const total = stat.size;
  const ext = path.extname(fp).toLowerCase();
  const mime = MIME[ext] || 'application/octet-stream';
  const range = req.headers.range;

  if (range) {
    const [s, e] = range.replace(/bytes=/, '').split('-');
    const start = parseInt(s, 10);
    const end = e ? parseInt(e, 10) : Math.min(start + 1024 * 1024, total - 1);
    res.writeHead(206, {
      'Content-Range': `bytes ${start}-${end}/${total}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': end - start + 1,
      'Content-Type': mime,
    });
    fs.createReadStream(fp, { start, end }).pipe(res);
  } else {
    res.writeHead(200, {
      'Content-Length': total,
      'Content-Type': mime,
      'Accept-Ranges': 'bytes',
    });
    fs.createReadStream(fp).pipe(res);
  }
});

// Export for Electron (starts on a random free port when port=0)
export function startServer(port = PORT) {
  return new Promise((resolve, reject) => {
    const srv = app.listen(port, '127.0.0.1', () => {
      const { port: actualPort } = srv.address();
      resolve(actualPort);
    });
    srv.on('error', reject);
  });
}

// Auto-start when run directly via `node server.js`
if (!process.versions.electron) {
  startServer(PORT).then(p => {
    console.log(`
╔══════════════════════════════════════════╗
║         🎵  Mediabox is running!         ║
╠══════════════════════════════════════════╣
║  Open in browser:                        ║
║  → http://localhost:${p}${' '.repeat(Math.max(0, 5 - String(p).length))}               ║
║                                          ║
║  First time? Go to Settings and add     ║
║  your Music / Videos folders.            ║
╚══════════════════════════════════════════╝
`);
  });
}
