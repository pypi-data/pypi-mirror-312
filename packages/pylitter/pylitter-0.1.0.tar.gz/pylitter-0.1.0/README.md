# litter

A simple CLI tool to upload temporary files to [Litterbox](https://litterbox.catbox.moe/) with an upload link.

Made for those who are too lazy to open SCP/SFTP.

## Installation
```
pip install pylitter
```

## Usage

You can use either Litterbox or Catbox (for permanent) for hosting. By default, it uses Litterbox.

```
litter <filename> --host=<host|default=litterbox> -t <time|1h/12h/24h/72h>
```

## Example
```
litter test.jpg -t 12h   

[71097/71097] bytes |====================>|
Your link : https://litter.catbox.moe/zmr6i6.jpg
```

## Running Tests
```
python3 upload_test.py
```

## Issues? Changes?
Just open an issue/pull requests