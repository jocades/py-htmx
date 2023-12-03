const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

const $inc = $("#inc-btn");
const $dec = $("#dec-btn");
const $counter = $("#counter");

$inc.addEventListener("click", () => {
  $counter.innerText = parseInt($counter.innerText) + 1;
});

$dec.addEventListener("click", () => {
  $counter.innerText = parseInt($counter.innerText) - 1;
});
