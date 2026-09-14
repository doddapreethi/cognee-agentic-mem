async function call(path, body = undefined) {
  const options = {
    method: body === undefined ? "GET" : "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
  };

  if (body !== undefined) {
    options.body = JSON.stringify(body);
  }

  let response;

  try {
    response = await fetch(path, options);
  } catch (error) {
    throw new Error(`Cannot connect to frontend server: ${error.message}`);
  }

  // Read the response as text first.
  // This lets us see the real server response if it is not JSON.
  const rawText = await response.text();

  let data;

  try {
    data = rawText ? JSON.parse(rawText) : {};
  } catch {
    console.error("Non-JSON server response:", rawText);

    throw new Error(
      `Invalid server response (HTTP ${response.status}).`
    );
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.error ||
      `HTTP ${response.status}`
    );
  }

  return data;
}


function show(id, value) {
  const element = document.getElementById(id);

  if (!element) {
    console.error(`Output element not found: ${id}`);
    return;
  }

  element.textContent = JSON.stringify(value, null, 2);
}


async function runButton(buttonId, outId, fn) {
  const button = document.getElementById(buttonId);

  if (!button) {
    console.error(`Button not found: ${buttonId}`);
    return;
  }

  button.disabled = true;

  try {
    const result = await fn();
    show(outId, result);
  } catch (error) {
    console.error(`${buttonId} error:`, error);

    show(outId, {
      error: error.message,
    });
  } finally {
    button.disabled = false;
  }
}


/*
 * IMPORTANT:
 * The browser talks to Node.js using /api/...
 * Node.js then adds the backend API token and
 * forwards the request to FastAPI.
 */


/* =========================
   RECALL
   ========================= */

document.getElementById("recallBtn").onclick = () =>
  runButton("recallBtn", "recallOut", async () => {
    const query = document.getElementById("query").value.trim();
    const topK = Number(document.getElementById("topK").value);

    if (!query) {
      throw new Error("Please enter a question.");
    }

    if (!Number.isInteger(topK) || topK < 1 || topK > 15) {
      throw new Error("Top K must be between 1 and 15.");
    }

    const data = await call("/api/memory/recall", {
      query,
      top_k: topK,
    });

    /*
     * Backend response shape:
     *
     * {
     *   "results": [...]
     * }
     */

    if (!data || !Object.prototype.hasOwnProperty.call(data, "results")) {
      console.error("Unexpected Recall response:", data);

      throw new Error(
        "Recall returned an unexpected response format."
      );
    }

    return data;
  });


/* =========================
   REMEMBER
   ========================= */

document.getElementById("rememberBtn").onclick = () =>
  runButton("rememberBtn", "rememberOut", async () => {
    const text = document
      .getElementById("rememberText")
      .value
      .trim();

    if (!text) {
      throw new Error("Please enter a memory to remember.");
    }

    return await call("/api/memory/remember", {
      text,
    });
  });


/* =========================
   INGEST SAMPLE
   ========================= */

document.getElementById("ingestBtn").onclick = () =>
  runButton("ingestBtn", "opsOut", () =>
    call("/api/memory/ingest-sample")
  );


/* =========================
   IMPROVE
   ========================= */

document.getElementById("improveBtn").onclick = () =>
  runButton("improveBtn", "opsOut", () =>
    call("/api/memory/improve")
  );


/* =========================
   FORGET
   ========================= */

document.getElementById("forgetBtn").onclick = async () => {
  const confirmed = confirm(
    "Delete the Cognee dataset private_memory? " +
    "The sample JSON source file will remain."
  );

  if (!confirmed) {
    return;
  }

  await runButton(
    "forgetBtn",
    "opsOut",
    () => call("/api/memory/forget")
  );
};