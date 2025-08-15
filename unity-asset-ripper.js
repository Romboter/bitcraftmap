import {spawn} from 'child_process';
import {EOL} from 'os';
import {request} from 'http';

const assetRipperPath = 'C:\\Users\\jaspe\\Downloads\\AssetRipper\\AssetRipper.GUI.Free.exe';
const assetFolderPath = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\BitCraft Online Demo';
const outPath = 'C:\\Users\\jaspe\\projects\\bitcraft-assets';

let port;

function startAssetRipperAndListenToStdOut(executablePath) {
    let buffer = '';

    const child = spawn(executablePath, [], {stdio: ['ignore', 'pipe', 'inherit'], windowsHide: true});
    child.stdout.setEncoding('utf8');

    child.stdout.on('data', async (chunk) => {
        buffer += chunk;
        const lines = buffer.split(EOL);
        buffer = lines.pop() || '';

        for (const line of lines) {
            await processStdOutLine(line);
        }
    });
}

const stdoutActions = [
    {
        match: /Now listening on: http:\/\/127\.0\.0\.1:(\d+)/,
        action: (match) => {
            port = match[1];
            console.log(`Port found: ${port}`);
            console.log(`Loading folder ${assetFolderPath}`);
            loadFolder(port, assetFolderPath);
        }
    },
    {
        match: /Processing : Finished processing assets/,
        action: () => {
            console.log('Folder loaded.');
            console.log(`Exporting files to ${outPath}`);
            exportPrimaryContent(port, outPath);
        }
    },
    {
        match: / : \((\d+)\/(\d+)\) Exporting '(.*)'/,
        action: (match) => {
            const [, index, total, file] = match;
            console.log(`Extracting file ${index} of ${total}: ${file}`);
        }
    }
];

async function processStdOutLine(line) {
    for (const {match, action} of stdoutActions) {
        const result = line.match(match);
        if (result) {
            action(result);
            break;
        }
    }
}

async function loadFolder(port, folderPath) {
    const body = new URLSearchParams({path: folderPath});
    post(port, '/LoadFolder', body);
}

async function exportPrimaryContent(port, outputFolderPath) {
    const body = new URLSearchParams({path: outputFolderPath});
    post(port, '/Export/PrimaryContent', body);
}

function post(port, path, body) {
    const req = request({
        hostname: '127.0.0.1',
        port,
        path,
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
    req.write(body.toString());
    req.end();
}

await startAssetRipperAndListenToStdOut(assetRipperPath);
