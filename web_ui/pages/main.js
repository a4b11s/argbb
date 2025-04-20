window.addEventListener("load", () => {
  const MODE_BTNS = document.getElementsByClassName("mode-btn");
  const SPEED_UP_BTN = document.getElementById("speed-up");
  const SPEED_DOWN_BTN = document.getElementById("speed-down");
  const PREV_COLOR_BTN = document.getElementById("prev-color");
  const NEXT_COLOR_BTN = document.getElementById("next-color");
  const SPEED_PROGRESS = document.getElementById("speed-progress");
  const MODE_CONFIG_CONTAINER = document.getElementById("mode-config");

  // Debounce utility function
  const debounce = (func, delay) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func(...args), delay);
    };
  };

  const renderModeConfig = () => {
    MODE_CONFIG_CONTAINER.innerHTML = ""; // Clear previous content
    fetch("/get_mode_config")
      .then((response) => response.json())
      .then((config) => {
        const tabNav = createTabNavigation();
        const tabContent = createTabContent();
        let activeTab = null;

        Object.keys(config).forEach((fieldName, index) => {
          const field = config[fieldName];
          const tabButton = createTabButton(field, () => {
            if (activeTab) activeTab.style.display = "none";
            tab.style.display = "flex";
            activeTab = tab;
          });

          const tab = createTab(field, fieldName);
          tab.style.display = index === 0 ? "flex" : "none";

          tabContent.appendChild(tab);
          tabNav.appendChild(tabButton);

          if (index === 0) {
            activeTab = tab;
            tabButton.classList.add("active");
          }
        });

        MODE_CONFIG_CONTAINER.appendChild(tabNav);
        MODE_CONFIG_CONTAINER.appendChild(tabContent);
      });
  };

  const createTabNavigation = () => {
    const tabNav = document.createElement("div");
    tabNav.className = "tab-nav";
    return tabNav;
  };

  const createTabContent = () => {
    const tabContent = document.createElement("div");
    tabContent.className = "tab-content";
    return tabContent;
  };

  const createTabButton = (field, onClick) => {
    const tabButton = document.createElement("button");
    tabButton.className = "tab-button";
    tabButton.textContent = field.name;
    tabButton.title = field.description;
    tabButton.addEventListener("click", (e) => {
      document
        .querySelectorAll(".tab-button")
        .forEach((btn) => btn.classList.remove("active"));
      e.target.classList.add("active");
      onClick();
    });
    return tabButton;
  };

  const createTab = (field, fieldName) => {
    const tab = document.createElement("div");
    tab.className = "config-tab";

    if (field.type === "color") {
      tab.appendChild(createColorPicker(field, fieldName));
    } else if (field.type === "array") {
      tab.appendChild(createMultiColorPicker(field, fieldName));
    } else if (field.type === "int" || field.type === "float") {
      tab.appendChild(createNumberInput(field, fieldName));
    }

    return tab;
  };

  const createColorPicker = (field, fieldName) => {
    const colorPickerContainer = document.createElement("div");
    const colorPicker = new iro.ColorPicker(colorPickerContainer, {
      width: 200,
      color: `rgb(${field.value[0]}, ${field.value[1]}, ${field.value[2]})`,
    });

    const debouncedUpdateConfig = debounce((fieldName, rgb) => {
      updateConfig(fieldName, [rgb.r, rgb.g, rgb.b]);
    }, 300);

    colorPicker.on("color:change", (color) => {
      const rgb = color.rgb;
      debouncedUpdateConfig(fieldName, rgb);
    });

    return colorPickerContainer;
  };

  const createMultiColorPicker = (field, fieldName) => {
    const container = document.createElement("div");
    const multiColorPicker = new iro.ColorPicker(container, {
      width: 300,
      colors: field.value.map(
        (color) => `rgb(${color[0]}, ${color[1]}, ${color[2]})`
      ),
    });

    const debouncedUpdateConfig = debounce((fieldName, colors) => {
      const rgbValues = colors.map((color) => [
        color.rgb.r,
        color.rgb.g,
        color.rgb.b,
      ]);
      updateConfig(fieldName, rgbValues);
    }, 300);

    multiColorPicker.on("color:change", () => {
      debouncedUpdateConfig(fieldName, multiColorPicker.colors);
    });

    const addButton = createAddButton(() => {
      multiColorPicker.addColor("rgb(255, 255, 255)");
      debouncedUpdateConfig(fieldName, multiColorPicker.colors);
    });

    const removeButton = createRemoveButton(() => {
      if (multiColorPicker.colors.length > 1) {
        multiColorPicker.removeColor(multiColorPicker.colors.length - 1);
        debouncedUpdateConfig(fieldName, multiColorPicker.colors);
      }
    });

    container.appendChild(addButton);
    container.appendChild(removeButton);

    return container;
  };

  const createRemoveButton = (onClick) => {
    const removeButton = document.createElement("button");
    removeButton.textContent = "Remove";
    removeButton.className = "remove-color-btn";
    removeButton.addEventListener("click", onClick);
    return removeButton;
  };

  const createAddButton = (onClick) => {
    const addButton = document.createElement("button");
    addButton.textContent = "Add Color";
    addButton.className = "add-color-btn";
    addButton.addEventListener("click", onClick);
    return addButton;
  };

  const createNumberInput = (field, fieldName) => {
    const input = document.createElement("input");
    input.type = "number";
    input.value = field.value;
    input.step = field.type === "float" ? "0.1" : "1";
    input.addEventListener("change", (e) => {
      updateConfig(fieldName, parseFloat(e.target.value));
    });
    return input;
  };

  // Function to update the configuration
  const updateConfig = (fieldName, value) => {
    fetch("/update_mode_config", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data: { [fieldName]: value } }),
    });
  };

  SPEED_UP_BTN.addEventListener("click", () => {
    fetch("/next_speed", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  });

  SPEED_DOWN_BTN.addEventListener("click", () => {
    fetch("/previous_speed", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  });

  PREV_COLOR_BTN.addEventListener("click", () => {
    fetch("/previous_color", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  });

  NEXT_COLOR_BTN.addEventListener("click", () => {
    fetch("/next_color", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  });

  SPEED_PROGRESS.addEventListener("change", (e) => {
    fetch("/set_speed", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ speed: 1000 - e.target.value }),
    });
  });

  for (let i = 0; i < MODE_BTNS.length; i++) {
    MODE_BTNS[i].addEventListener("click", (e) => {
      fetch("/set_mode", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mode: e.target.id }),
      });

      renderModeConfig();
    });
    SPEED_PROGRESS.value = 500;
  }

  renderModeConfig();
});
