## Files Downloader

Python script that downloads files from the internet and saves them in a download directory.

The list of URLs to download will be provided in a simple text file.
URLs are separated by a newline. Assume that the files are small, so downloading them does not require streaming.

Example input.txt:
```
https://cdn-9.motorsport.com/images/mgl/24vA3r46/s500/max-verstappen-red-bull-racing-1.webp
https://cdn-8.motorsport.com/images/mgl/24vA4nA6/s500/daniel-ricciardo-mclaren-1.webp
https://cdn-8.motorsport.com/images/mgl/0L1nLWJ2/s500/lando-norris-mclaren-1.webp
```

The download directory should be provided as a command line parameter.

Consider the following and implement reasonable solutions for the following problems:

### Considered issues

> How to handle HTTP 404 errors?

Handled by checking status code and only responses that have 200 are Successful

> How to make the download process faster?

Async programing solve this issue. The hard limit is set by aiohttp which set
connection numbers to 100 by default. But also it could be configured by CLI
param
(REF: https://docs.aiohttp.org/en/latest/http_request_lifecycle.html#how-to-use-the-clientsession)

> How to display the progress of downloads?

`await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)` and especially
`asyncio.FIRST_COMPLETED` make it possible

> How to handle cancellation? (i.e., the user presses CTRL+C)

As I'm using event loop there is no problem with handling leftover python processes
as it could be if I would spawn separate processes for download

> Optional: How to handle retry in case of intermittent network errors?

Based on which exception is understood as retryable there is a retry functionality.
Implementation an exponential backoff retry strategy would be even better comparing
with constant time sleep
