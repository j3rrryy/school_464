const mybutton = document.getElementById("btn-back-to-top");

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

function backToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

window.onscroll = scrollFunction;
mybutton.addEventListener("click", backToTop);

// ======================

const allElements = document.querySelectorAll("*");
const root = document.documentElement;
const variables = {
    "--vis-imp-1-0": getComputedStyle(root).getPropertyValue("--vis-imp-1-0"),
    "--vis-imp-1-1": getComputedStyle(root).getPropertyValue("--vis-imp-1-1"),
    "--vis-imp-2-0": getComputedStyle(root).getPropertyValue("--vis-imp-2-0"),
    "--vis-imp-2-1": getComputedStyle(root).getPropertyValue("--vis-imp-2-1"),
    "--vis-imp-3-0": getComputedStyle(root).getPropertyValue("--vis-imp-3-0"),
    "--vis-imp-3-1": getComputedStyle(root).getPropertyValue("--vis-imp-3-1"),
};

// ======================

function saveTheme(theme, fontSize) {
    localStorage.setItem("accessibilityTheme", theme);
    localStorage.setItem("fontSize", fontSize);
}

function applyTheme(theme) {
    allElements.forEach(e => {
        if (e.hasAttribute("data-fixed-colors")) return;
        switch (theme) {
            case "default":
                e.style.backgroundColor = e.getAttribute("data-original-background-color");
                e.style.color = e.getAttribute("data-original-color");
                break;
            case "whiteOnBlack":
                e.style.setProperty("background-color", "#000000", "important");
                e.style.setProperty("color", "#ffffff", "important");
                break;
            case "darkBlueOnLightBlue":
                e.style.setProperty("background-color", variables["--vis-imp-1-0"], "important");
                e.style.setProperty("color", variables["--vis-imp-1-1"], "important");
                break;
            case "brownOnBeige":
                e.style.setProperty("background-color", variables["--vis-imp-2-0"], "important");
                e.style.setProperty("color", variables["--vis-imp-2-1"], "important");
                break;
            case "greenOnDarkBrown":
                e.style.setProperty("background-color", variables["--vis-imp-3-0"], "important");
                e.style.setProperty("color", variables["--vis-imp-3-1"], "important");
                break;
        }
    });
}

// ======================

allElements.forEach(e => {
    e.dataset.originalBackgroundColor = window.getComputedStyle(e).backgroundColor;
    e.dataset.originalColor = window.getComputedStyle(e).color;
});

// ======================

function setFontSize(newSize) {
    document.documentElement.style.fontSize = newSize + "px";
    saveTheme(localStorage.getItem("accessibilityTheme") || "default", newSize);
}

function changeFont(delta) {
    let font = parseInt(window.getComputedStyle(document.documentElement).fontSize);
    font = Math.min(24, Math.max(12, font + delta));
    setFontSize(font);
}

// ======================

document.getElementById("increaseFontBtn").addEventListener("click", () => changeFont(2));
document.getElementById("normalFontBtn").addEventListener("click", () => setFontSize(""));
document.getElementById("decreaseFontBtn").addEventListener("click", () => changeFont(-2));

const themeButtons = {
    defaultColorBtn: "default",
    whiteOnBlackBtn: "whiteOnBlack",
    darkBlueOnLightBlueBtn: "darkBlueOnLightBlue",
    brownOnBeigeBtn: "brownOnBeige",
    greenOnDarkBrownBtn: "greenOnDarkBrown"
};

Object.entries(themeButtons).forEach(([btnId, theme]) => {
    const btn = document.getElementById(btnId);
    btn.addEventListener("click", () => {
        applyTheme(theme);
        saveTheme(theme, window.getComputedStyle(document.documentElement).fontSize.replace("px", ""));
    });
});

// ======================

window.onload = () => {
    const theme = localStorage.getItem("accessibilityTheme") || "default";
    const fontSize = localStorage.getItem("fontSize");
    applyTheme(theme);
    if (fontSize) document.documentElement.style.fontSize = fontSize + "px";
};
