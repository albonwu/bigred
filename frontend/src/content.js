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
    const audio = document.createElement("audio");
    audio.preload = "none";
    parentElement.insertBefore(audio, equationDiv);
    // equationDiv.prepend(audio);
    equationDiv.addEventListener("click", async () => {
      const tex = MathMLToLaTeX.convert(mathMl);
      const response = await fetch(`${BACKEND}?tex=${tex}`);
      const signedUrl = await response.text();
      console.log("signedUrl", signedUrl);
      audio.src = signedUrl;
      audio.controls = true;
    });
  }
}

main();
