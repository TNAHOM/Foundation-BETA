const clearInputText = (other) => {
  const inputTexts = document.querySelectorAll("input[type='text'][name='" + other + "']");
  inputTexts.forEach((inputText) => {
    inputText.value = '';
  });
};

const clearSelection = (name, other) => {
  const radioBtns = document.querySelectorAll(
  "input[type='radio'][name='" + name + "']"
  );
  radioBtns.forEach((radioBtn) => {
    if (radioBtn.checked === true) radioBtn.checked = false;
  });
  clearInputText(other)
};