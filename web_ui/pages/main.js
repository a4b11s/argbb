window.addEventListener("load", () => {
  const MODE_BTNS = document.getElementsByClassName("mode-btn");
  const SPEED_UP_BTN = document.getElementById("speed-up");
  const SPEED_DOWN_BTN = document.getElementById("speed-down");
  const PREV_COLOR_BTN = document.getElementById("prev-color");
  const NEXT_COLOR_BTN = document.getElementById("next-color");
  const SPEED_PROGRESS = document.getElementById("speed-progress");

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
    });
    SPEED_PROGRESS.value = 500;
  }

  const colorPicker = new iro.ColorPicker("#picker", {
    width: 500,
    color: "#f00",
  });

  const debounce = (func, delay) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func(...args), delay);
    };
  };

  const sendColorChange = debounce((color) => {
    fetch("/set_color", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ color: color.hexString }),
    });
  }, 300);

  colorPicker.on("color:change", (color) => {
    sendColorChange(color);
  });
});
