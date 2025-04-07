window.addEventListener("load", () => {
    const NAME_INPUT = document.getElementById("name");
    const PIN_LED_INPUT = document.getElementById("led_pin");
    const NUM_LED_INPUT = document.getElementById("num_leds");
    const SAVE_BTN = document.getElementById("save");
    const UPDATE_BTN = document.getElementById("update");

    let name = "";
    let pin_led = "";
    let num_led = "";

    NAME_INPUT.addEventListener("input", (e) => {
        name = e.target.value;
    });
    PIN_LED_INPUT.addEventListener("input", (e) => {
        pin_led = e.target.value;
    });
    NUM_LED_INPUT.addEventListener("input", (e) => {
        num_led = e.target.value;
    });
    SAVE_BTN.addEventListener("click", () => {
        const data = {
            name: name,
            pin_led: pin_led,
            num_led: num_led,
        };

        console.log("Saving settings:", data);
    });

    UPDATE_BTN.addEventListener("click", () => {
        console.log("Updating firmware...");
    });
});
