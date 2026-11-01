// This application policy complements the container mount boundary. Open mode
// can execute processes and therefore does not treat this file as a sandbox.
import {mkdirSync, writeFileSync} from 'node:fs';
import {homedir} from 'node:os';
import {join} from 'node:path';
const directory = join(homedir(), '.claude-server-commander');
mkdirSync(directory, {recursive: true, mode: 0o700});
writeFileSync(join(directory, 'config.json'), JSON.stringify({
  allowedDirectories: ['/workspace'],
  telemetryEnabled: false,
}), {mode: 0o600});
