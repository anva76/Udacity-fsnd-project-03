# Coffee Shop Frontend

## Overview

The frontend part was already pre-built using the Ionic framework.

## Getting Setup

### Prerequisites

* **Installing Node and NPM** - This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

* **Ionic CLI** - The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

### Installing Dependencies

In your terminal, please navigate to the `/frontend` folder and run:

```bash
npm install
```

## Running Frontend in Development Mode

Ionic uses a configuration file to manage environment variables. Please open `./src/environments/environments.ts` and ensure each variable corresponds to your backend configuration.

In your terminal, please navigate to the `/frontend` folder and run the following command to start the frontend development server:

```bash
NODE_OPTIONS=--openssl-legacy-provider bash -c 'ionic serve'
```
> Please note that the option `--openssl-legacy-provider` may be required for compatibility reasons in order to launch it on newer versions of Node.js.

Open http://localhost:8100/ in your browser to run the Coffee shop app.

