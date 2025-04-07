window.addEventListener("load", () => {
  const NAME_INPUT = document.getElementById("name");
  const PIN_LED_INPUT = document.getElementById("led_pin");
  const NUM_LEDS_INPUT = document.getElementById("num_leds");
  const SAVE_BTN = document.getElementById("save-settings");
  const UPDATE_BTN = document.getElementById("update");

  let name = "";
  let pin_led = "";
  let num_leds = "";

  NAME_INPUT.addEventListener("input", (e) => {
    name = e.target.value;
  });
  PIN_LED_INPUT.addEventListener("input", (e) => {
    pin_led = e.target.value;
  });
  NUM_LEDS_INPUT.addEventListener("input", (e) => {
    num_leds = e.target.value;
  });
  SAVE_BTN.addEventListener("click", () => {
    const data = {};
    if (name) data.name = name;
    if (pin_led) data.pin_led = pin_led;
    if (num_leds) data.num_leds = num_leds;

    if (Object.keys(data).length > 0) {
      fetch("/set_config", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ data }),
      });
    }
  });

  UPDATE_BTN.addEventListener("click", () => {
    fetch("/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  });
});
