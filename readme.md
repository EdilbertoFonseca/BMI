# Body Mass Index (BMI) Calculation

* **Author**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Creation Date**: 11/08/2022.
* **Version**: 2026.2.1
* **License**: [GPL v2](https://www.gnu.org/licenses/gpl-2.0.html)
* **Last Revised**: 04/05/2026

## Introduction

Welcome to the BMI Add-on! This is a plug-in designed to help determine Body Mass Index (BMI), an international measure used to assess a person’s body fat level. With this add-on, you can easily calculate your BMI by entering your height and weight.

In addition to the traditional BMI calculation, this new version offers additional features, such as calculating the ideal BMI based on height and providing a detailed classification according to the criteria of the World Health Organization (WHO), offering personalized health guidance. The add-on now also saves the last 10 calculations, which can be quickly accessed using the Alt+H shortcut.

Note: For a proper interpretation of BMI, it's important to consider other factors such as body composition, fat distribution, age, sex, and overall health. It is always advisable to consult a healthcare professional, such as a doctor or nutritionist, for a more accurate assessment and appropriate health and weight guidance.

## Installation

Here are the step-by-step instructions to install the BMI Add-on in NVDA:

1. In NVDA, open the **Tools** menu and look for the **Add-on Store**.
2. In the **Available Add-ons** tab, navigate to the **Search** field.
3. Search for "BMI". In the results, press **Enter** or **Apply**, then select **Install**.
4. Restart NVDA to apply the changes.

You're now ready to use the BMI Add-on and calculate your Body Mass Index directly in NVDA.

## Settings

There are no configuration instructions for the add-on, as its use is straightforward.

## Usage

Press `Alt+Windows+I`, or use the NVDA menu `NVDA+N`, Tools > Calculate your BMI, to launch the add-on. A dialog with two input fields will appear:

1. Height – where your height in centimeters (CM) should be selected or entered.
2. Weight – where your weight in kilograms (KG) should be selected or entered.

After filling in all fields, press the Calculate button using the shortcut `Alt+A`, or press Enter on the calculate button.

NVDA will read out a dialog containing:

* The result of your current BMI calculation.
* Your detailed classification according to WHO parameters (underweight, normal weight, overweight, obesity grade I, II, or III).
* The estimated value of your ideal BMI based on your height.
* A guidance message emphasizing the importance of additional factors in health assessment.

At the end of the dialog, the cursor will be positioned on the OK button. Pressing Enter will reposition the cursor to the height field.

## Keyboard Shortcuts

### Main Dialog

* `Alt+A`: Performs the BMI calculation.
* `Alt+L`: Clears the fields and places the cursor in the height field.
* `Alt+H`: Displays the calculation history.
* `Alt+C`: Closes the dialog (you can also use the Esc key).

## Acknowledgments

Special thanks to the contributors Rui Fonte, Noelia, and Dalen, whose help made this project possible.

## Translation

Translations for this add-on are managed through the [NVDA Add-ons Crowdin project](https://crowdin.com/project/nvdaaddons).

To contribute a translation, create a Crowdin account, join the appropriate language team if required, and translate the available interface and documentation strings directly in Crowdin.

You can also use Poedit to work with `.po` and `.xliff` files locally. Completed translations are synchronized to the add-on repository through the localization workflow.

For questions or assistance, please join the [NVDA Translations mailing list](https://groups.io/g/nvda-translations).
