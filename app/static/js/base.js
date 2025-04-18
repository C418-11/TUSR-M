
function getTheme(defaultVal){
    let theme = localStorage.getItem("theme");
    if (theme !== null) {
        return theme;
    }
    theme = document.documentElement.getAttribute("data-theme");
    if (theme !== null) {
        return theme;
    }
    return defaultVal;
}

function nextTheme(theme) {
    let index = Themes.indexOf(theme);
    index = (index + 1) % Themes.length;
    return Themes[index];
}

function initTheme() {
    let theme = getTheme(Themes[0]);

    // 暂时设渐变时间为0s
    let transitionDuration = document.documentElement.style.getPropertyValue("--transition-duration");
    document.documentElement.style.setProperty("--transition-duration", "0s");
    requestAnimationFrame(() => {
        // 设置主题
        document.documentElement.setAttribute("data-theme", theme);
        requestAnimationFrame(() => {
            // 恢复渐变时间
            document.documentElement.style.setProperty("--transition-duration", transitionDuration);
        });
    });
}

initTheme();

window.addEventListener("DOMContentLoaded", () => {
    let themeSwitcher = document.getElementById("theme-switcher-button");
    if (themeSwitcher) {
        themeSwitcher.addEventListener("click", toggleTheme);
    }
    updateTheme();
});

function toggleTheme() {
    let theme = nextTheme(getTheme(Themes[-1]));

    // 设置主题
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    updateTheme();
}

function updateTheme() {
    let theme = getTheme(Themes[0]);

    // 设置主题图标
    let themeData = ThemeDatas[theme];
    let themeIcon = document.getElementById("theme-switcher-icon");

    if (themeIcon) {
        themeIcon.src = themeData.icon;
        themeIcon.alt = themeData.desc;
    }

    // 获取下个主题
    let nextThemeData = ThemeDatas[nextTheme(theme)];

    // 下个主题预览
    let themePreview = document.getElementById("theme-switcher-preview");
    if (themePreview) {
        themePreview.src = nextThemeData.icon;
        themePreview.alt = nextThemeData.desc;
    }
}
