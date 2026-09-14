import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

dotenv.config({
  path: path.resolve(process.cwd(), "../.env"),
});

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PUBLIC_DIR = path.join(__dirname, "public");

const FRONTEND_HOST =
  process.env.FRONTEND_HOST || "127.0.0.1";

const FRONTEND_PORT =
  Number(process.env.FRONTEND_PORT) || 3000;

const BACKEND_URL =
  process.env.BACKEND_URL || "http://127.0.0.1:8000";

const BACKEND_API_TOKEN =
  process.env.BACKEND_API_TOKEN;

if (!BACKEND_API_TOKEN) {
  throw new Error(
    "BACKEND_API_TOKEN is missing from the root .env file."
  );
}


const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
};


function sendJson(res, statusCode, data) {
  const body = JSON.stringify(data);

  res.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body),
  });

  res.end(body);
}


function serveStatic(res, pathname) {
  let filePath;

  if (pathname === "/") {
    filePath = path.join(PUBLIC_DIR, "index.html");
  } else {
    filePath = path.join(
      PUBLIC_DIR,
      pathname.replace(/^\/+/, "")
    );
  }

  // Prevent path traversal.
  const normalizedPublicDir = path
    .resolve(PUBLIC_DIR)
    .toLowerCase();

  const normalizedFilePath = path
    .resolve(filePath)
    .toLowerCase();

  if (!normalizedFilePath.startsWith(normalizedPublicDir)) {
    sendJson(res, 403, {
      error: "Forbidden",
    });
    return;
  }

  fs.readFile(filePath, (error, data) => {
    if (error) {
      sendJson(res, 404, {
        error: "Not Found",
      });
      return;
    }

    const extension = path.extname(filePath).toLowerCase();

    res.writeHead(200, {
      "Content-Type":
        MIME_TYPES[extension] ||
        "application/octet-stream",
    });

    res.end(data);
  });
}


function readRequestBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";

    req.on("data", (chunk) => {
      body += chunk.toString();

      // Safety limit: 1 MB request body.
      if (body.length > 1024 * 1024) {
        reject(
          new Error("Request body too large.")
        );

        req.destroy();
      }
    });

    req.on("end", () => {
      resolve(body);
    });

    req.on("error", reject);
  });
}


async function proxyToBackend(req, res, pathname) {
  try {
    const backendPath = pathname.replace(
      /^\/api/,
      ""
    );

    const backendUrl =
      `${BACKEND_URL}${backendPath}`;

    const body =
      req.method === "GET" ||
      req.method === "HEAD"
        ? undefined
        : await readRequestBody(req);

    console.log(
      `[PROXY] ${req.method} ${pathname} -> ${backendUrl}`
    );

    const backendResponse = await fetch(
      backendUrl,
      {
        method: req.method,

        headers: {
          "x-api-key": BACKEND_API_TOKEN,

          "Content-Type":
            req.headers["content-type"] ||
            "application/json",

          "Accept":
            req.headers["accept"] ||
            "application/json",
        },

        body,
      }
    );

    const responseText =
      await backendResponse.text();

    res.writeHead(
      backendResponse.status,
      {
        "Content-Type":
          backendResponse.headers.get(
            "content-type"
          ) ||
          "application/json; charset=utf-8",
      }
    );

    res.end(responseText);

  } catch (error) {
    console.error(
      "[PROXY ERROR]",
      error
    );

    sendJson(res, 502, {
      error: "Backend unavailable",
      detail: error.message,
    });
  }
}


const server = http.createServer(
  async (req, res) => {
    try {
      const url = new URL(
        req.url,
        `http://${req.headers.host || "localhost"}`
      );

      const pathname = url.pathname;

      /*
       * API PROXY
       *
       * Browser:
       * /api/memory/recall
       *
       * Node:
       * /memory/recall
       *
       * FastAPI:
       * http://127.0.0.1:8000/memory/recall
       */

      if (pathname.startsWith("/api/")) {
        await proxyToBackend(
          req,
          res,
          pathname
        );
        return;
      }


      /*
       * STATIC FRONTEND
       */

      if (
        req.method === "GET" ||
        req.method === "HEAD"
      ) {
        serveStatic(
          res,
          pathname
        );
        return;
      }


      sendJson(res, 405, {
        error: "Method Not Allowed",
      });

    } catch (error) {
      console.error(
        "[SERVER ERROR]",
        error
      );

      sendJson(res, 500, {
        error: "Internal Server Error",
      });
    }
  }
);


server.listen(
  FRONTEND_PORT,
  FRONTEND_HOST,
  () => {
    console.log("");
    console.log(
      "========================================"
    );
    console.log(
      "       PRIVATE COGNEE MEMORY UI"
    );
    console.log(
      "========================================"
    );
    console.log(
      `Frontend : http://${FRONTEND_HOST}:${FRONTEND_PORT}`
    );
    console.log(
      `Backend  : ${BACKEND_URL}`
    );
    console.log(
      "API proxy: /api/* -> backend"
    );
    console.log(
      "========================================"
    );
    console.log("");
  }
);