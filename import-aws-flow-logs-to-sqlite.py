'''
    import-aws-flow-logs-to-sqlite.py - A script to process AWS flow logs stdin to a sqlite database
    Copyright (C) 2018 Rowan Wookey <admin@rwky.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import argparse
import sys
import sqlite3

parser = argparse.ArgumentParser(description='Process AWS flow logs stdin to a sqlite database (use zcat files.gz | to pipe into this script)')
parser.add_argument('--file', '-f', help='Database file to create', required=True)
args = parser.parse_args()
conn = sqlite3.connect(args.file)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    date TEXT,
    version INT,
    account_id TEXT,
    interface_id TEXT, 
    srcaddr TEXT,
    dstaddr TEXT,
    srcport INT,
    dstport INT,
    protocol INT,
    packets INT,
    bytes INT,
    start INT,
    end INT,
    action TEXT,
    log_status TEXT
);
''')
cursor.execute('''
CREATE INDEX IF NOT EXISTS interface ON logs (interface_id);
''')
cursor.execute('''
CREATE INDEX IF NOT EXISTS start_end ON logs (start, end);
''')
cursor.execute('''
CREATE INDEX IF NOT EXISTS addr_and_port ON logs (srcaddr, dstaddr, srcport, dstport);
''')
for line in sys.stdin:
    line = line.strip()
    fields = line.split(' ')
    cursor.execute('INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', fields)

conn.commit()
conn.close()
