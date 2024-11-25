// Event listener for the Text Input card
document.querySelector('.card[data-id="1"]').addEventListener('click', () => {
    const textInput = prompt("Enter your text data:");
    if (textInput) {
        console.log("Text Input:", textInput);
        alert("Text data saved: " + textInput);
        // You can store this data or send it to a server for processing
    } else {
        alert("No input provided!");
    }
});

// Event listener for the Custom Input card
document.querySelector('.card[data-id="2"]').addEventListener('click', () => {
    let customInputs = [];
    let addMore = true;

    while (addMore) {
        const input = prompt("Enter custom input in the format [Text Input]:[Numeric Input] (e.g., Example:42):");
        if (input && input.includes(":")) {
            customInputs.push(input);
            addMore = confirm("Do you want to add another input?");
        } else {
            alert("Invalid input. Please use the format [Text Input]:[Numeric Input].");
            addMore = confirm("Do you want to try again?");
        }
    }

    if (customInputs.length > 0) {
        console.log("Custom Inputs:", customInputs);
        alert("Custom inputs saved:\n" + customInputs.join("\n"));
        // You can store these inputs or send them to a server for processing
    } else {
        alert("No custom inputs provided!");
    }
});

// Event listener for the CSV Input card
document.querySelector('.card[data-id="3"]').addEventListener('click', () => {
    // Create an input element for file uploads
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.csv';
    fileInput.style.display = 'none';

    // Append to the body temporarily
    document.body.appendChild(fileInput);

    // Trigger the file input click
    fileInput.click();

    // Handle file selection
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            console.log("CSV File:", file);
            alert(`CSV file uploaded: ${file.name}`);
            // You can send this file to a server or process it further here
        } else {
            alert("No file selected!");
        }

        // Remove the input element from the DOM
        document.body.removeChild(fileInput);
    });
});
 