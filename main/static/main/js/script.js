// back to top button
let mybutton = document.getElementById("btn-back-to-top");

window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

// version for visually impaired
const allElements = document.querySelectorAll('*');
const root = document.documentElement;
const variables = {
  '--vis-imp-1-0': getComputedStyle(root).getPropertyValue('--vis-imp-1-0'),
  '--vis-imp-1-1': getComputedStyle(root).getPropertyValue('--vis-imp-1-1'),
  '--vis-imp-2-0': getComputedStyle(root).getPropertyValue('--vis-imp-2-0'),
  '--vis-imp-2-1': getComputedStyle(root).getPropertyValue('--vis-imp-2-1'),
  '--vis-imp-3-0': getComputedStyle(root).getPropertyValue('--vis-imp-3-0'),
  '--vis-imp-3-1': getComputedStyle(root).getPropertyValue('--vis-imp-3-1')
};
allElements.forEach(element => {
  element.dataset.originalBackgroundColor = window.getComputedStyle(element).backgroundColor;
  element.dataset.originalColor = window.getComputedStyle(element).color;
});

const increaseFontBtn = document.getElementById('increaseFontBtn');
const normalFontBtn = document.getElementById('normalFontBtn');
const decreaseFontBtn = document.getElementById('decreaseFontBtn');
const defaultColorBtn = document.getElementById('defaultColorBtn');
const whiteOnBlackBtn = document.getElementById('whiteOnBlackBtn');
const blackOnWhiteBtn = document.getElementById('blackOnWhiteBtn');
const darkBlueOnLightBlueBtn = document.getElementById('darkBlueOnLightBlueBtn');
const brownOnBeigeBtn = document.getElementById('brownOnBeigeBtn');
const greenOnDarkBrownBtn = document.getElementById('greenOnDarkBrownBtn');


increaseFontBtn.addEventListener('click', () => {
  let currentSize = parseInt(window.getComputedStyle(document.documentElement).fontSize);
  currentSize = Math.min(24, currentSize + 2);
  document.documentElement.style.fontSize = currentSize + 'px';
});

normalFontBtn.addEventListener('click', () => {
  document.documentElement.style.fontSize = '';
});

decreaseFontBtn.addEventListener('click', () => {
  let currentSize = parseInt(window.getComputedStyle(document.documentElement).fontSize);
  currentSize = Math.max(12, currentSize - 2);
  document.documentElement.style.fontSize = currentSize + 'px';
});

defaultColorBtn.addEventListener('click', () => {
  allElements.forEach(element => {
    element.style.backgroundColor = element.getAttribute("data-original-background-color");
    element.style.color = element.getAttribute("data-original-color");
  });
});


blackOnWhiteBtn.addEventListener('click', () => {
  allElements.forEach(element => {
    element.style.backgroundColor = '#000000';
    element.style.color = '#ffffff';
  });
});

darkBlueOnLightBlueBtn.addEventListener('click', () => {
  allElements.forEach(element => {
    element.style.backgroundColor = variables['--vis-imp-1-0'];
    element.style.color = variables['--vis-imp-1-1'];
  });
});

brownOnBeigeBtn.addEventListener('click', () => {
  allElements.forEach(element => {
    element.style.backgroundColor = variables['--vis-imp-2-0'];
    element.style.color = variables['--vis-imp-2-1'];
  });
});

greenOnDarkBrownBtn.addEventListener('click', () => {
  allElements.forEach(element => {
    element.style.backgroundColor = variables['--vis-imp-3-0'];
    element.style.color = variables['--vis-imp-3-1'];
  });
});
