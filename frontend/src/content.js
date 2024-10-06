import { MathMLToLaTeX } from "mathml-to-latex";

console.log("hello world from the eq -> speech extension!");
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
      if (window.loadingTexToSpeech || equationDiv.dataset.generated) {
        return;
      }
      window.loadingTexToSpeech = true;
      div.appendChild(loadingElement);

      const tex = MathMLToLaTeX.convert(mathMl);
      const response = await fetch(`${BACKEND}?tex=${tex}`);
      const signedUrl = await response.text();
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
