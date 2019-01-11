# IDA Mirador Proxy
Lightweight flask app to serve manifests via Mirador. The app accepts a manifest and (optional) canvas parameter to automatically load a specific manifest into an instance of the latest Mirador.

The Dockerfile will build Mirador as part of the build process.


## Installation
The service provides a Dockerfile which uses uWSGI to run a Flask app to provide the Mirador proxy service.

```bash
docker build -t mirador-proxy .
docker run -p 3000:80000 mirador-proxy:latest
```

The shell script above will spin up the service on port 3000.

## Contribution Guidelines
ida-mirador-proxy has been tested using Python 3.6+.

Feel free to raise Github issues.

If you find an issue you are interested in fixing you can:

Fork the repository
Clone the repository to your local machine
Create a new branch for your fix using git checkout -b branch-name-here.
Fix the issue.
Commit and push the code to your remote repository.
Submit a pull request to the ida-mirador-proxy repository, with a description of your fix and the issue number.
The PR will be reviewed by the maintainer https://github.com/mattmcgrattan and either merge the PR or response with comments.
Thanks!

## License

MIT License

Copyright (c) Digirati 2018

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
