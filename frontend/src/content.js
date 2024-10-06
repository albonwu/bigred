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
    console.log("equationDiv", equationDiv);
    const mathMl = equationDiv.querySelector(
      'script[type="math/mml"]'
    )?.innerHTML;
    if (!mathMl) {
      continue;
    }
    equationDiv.addEventListener("click", () => {
      const tex = MathMLToLaTeX.convert(mathMl);
      fetch(BACKEND, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tex }),
      }).then((data) => console.log("data", data));
    });
  }
}
// bro wtf: https://mathjax.github.io/MathJax-demos-web/speech-generator/convert-with-speech.html

main();
