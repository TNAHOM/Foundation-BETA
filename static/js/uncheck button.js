const clearSelection = (name) => {
  const radioBtns = document.querySelectorAll(
  "input[type='radio'][name='" + name + "']"
  );
  radioBtns.forEach((radioBtn) => {
    if (radioBtn.checked === true) radioBtn.checked = false;
  });
};