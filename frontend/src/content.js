import { MathMLToLaTeX } from "mathml-to-latex";
import { PinataSDK } from "pinata";
import { PINATA_GATEWAY, PINATA_KEY } from "./key";

const pinata = new PinataSDK({
  pinataJwt: PINATA_KEY,
  pinataGateway: PINATA_GATEWAY,
});

console.log("hello world from the eq -> speech extension!");
async function findFileWithTex(tex) {
  const options = {
    method: "GET",
    headers: { Authorization: `Bearer ${PINATA_KEY}` },
  };

  console.log("tex", tex);
  const endpoint = `https://api.pinata.cloud/v3/files?metadata[tex]=${tex}`;
  console.log("endpoint", endpoint);
  const response = await fetch(endpoint, options);
  const responseJson = await response.json();
  console.log("responseJson", responseJson);
  if (responseJson.data.files.length != 0) {
    const cid = responseJson.data.files[0].cid;
    console.log("cid", cid);
    const url = await pinata.gateways.createSignedURL({
      cid,
      expires: 24 * 3600,
    });
    console.log("url", url);
    return url;
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function msFrom(date) {
  return new Date().getTime() - date.getTime();
}
const timeoutMs = 20 * 1000;
const sleepMs = 1000;
const BACKEND = "http://127.0.0.1:5000";

async function main() {
  let equationDivs = document.querySelectorAll("div[data-type=equation]");
  const startDate = new Date();

  while (msFrom(startDate) < timeoutMs) {
    console.log("refresh");
    equationDivs = document.querySelectorAll("div[data-type=equation]");
    if (equationDivs.length === 0) {
      await sleep(sleepMs);
    } else {
      break;
    }
  }

  if (equationDivs.length === 0) {
    console.log("no equations found!");
    return;
  }
  console.log("equationDivs", equationDivs);

  for (const equationDiv of equationDivs) {
    const mathMl = equationDiv.querySelector(
      'script[type="math/mml"]'
    )?.innerHTML;
    if (!mathMl) {
      continue;
    }
    const parentElement = equationDiv.parentElement;
    const div = document.createElement("div");
    div.style.width = "100%";
    div.style.display = "flex";
    div.style["flex-direction"] = "column";
    div.style["align-items"] = "center";

    parentElement.insertBefore(div, equationDiv);
    let loadingElement = document.createElement("i");
    loadingElement.innerText = "Loading...";
    // equationDiv.prepend(audio);
    const audio = document.createElement("audio");
    audio.controls = true;
    audio.autoplay = true;
    equationDiv.addEventListener("click", async () => {
      // todo: check for pinata existing before sending
      if (window.loadingTexToSpeech || equationDiv.dataset.generated) {
        return;
      }

      window.loadingTexToSpeech = true;
      div.appendChild(loadingElement);
      const tex = MathMLToLaTeX.convert(mathMl);

      let signedUrl = await findFileWithTex(tex);
      if (!signedUrl) {
        console.log("no file found, making new!");
        const response = await fetch(`${BACKEND}?tex=${tex}`);
        signedUrl = await response.text();
      }

      console.log("signedUrl", signedUrl);

      loadingElement = div.removeChild(loadingElement);
      audio.src = signedUrl;
      div.appendChild(audio);
      equationDiv.ariaLabel = tex;
      equationDiv.dataset.generated = true;
      window.loadingTexToSpeech = false;
    });
  }
}

main();
