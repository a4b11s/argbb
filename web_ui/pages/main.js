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
        // Create a tab navigation container
        const tabNav = document.createElement("div");
        tabNav.className = "tab-nav";

        // Create a content container for tabs
        const tabContent = document.createElement("div");
        tabContent.className = "tab-content";

        // Track active tab
        let activeTab = null;

        Object.keys(config).forEach((fieldName, index) => {
          const field = config[fieldName];

          // Create a tab button
          const tabButton = document.createElement("button");
          tabButton.className = "tab-button";
          tabButton.textContent = field.name;
          tabButton.title = field.description;

          // Create a tab content container
          const tab = document.createElement("div");
          tab.className = "config-tab";
          tab.style.display = index === 0 ? "block" : "none"; // Show the first tab by default

          // Add input based on the field type
          if (field.type === "color") {
            const colorPicker = new iro.ColorPicker(tab, {
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

            colorPicker.on("color:change", (color) => {
              const rgb = color.rgb;
              updateConfig(fieldName, [rgb.r, rgb.g, rgb.b]);
            });
          } else if (field.type === "int" || field.type === "float") {
            const input = document.createElement("input");
            input.type = "number";
            input.value = field.value;
            input.step = field.type === "float" ? "0.1" : "1";
            input.addEventListener("change", (e) => {
              updateConfig(fieldName, parseFloat(e.target.value));
            });
            tab.appendChild(input);
          }

          // Append the tab content to the content container
          tabContent.appendChild(tab);

          // Add click event to switch tabs
          tabButton.addEventListener("click", () => {
            if (activeTab) {
              activeTab.style.display = "none";
            }
            tab.style.display = "block";
            activeTab = tab;
          });

          // Append the tab button to the navigation
          tabNav.appendChild(tabButton);

          // Set the first tab as active by default
          if (index === 0) {
            activeTab = tab;
          }
        });

        // Append the navigation and content containers to the main container
        MODE_CONFIG_CONTAINER.appendChild(tabNav);
        MODE_CONFIG_CONTAINER.appendChild(tabContent);
      });
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
