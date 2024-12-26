 
// Event listener for the Text Input card
document.querySelector('.card[data-id="1"]').addEventListener('click', () => {
    window.location.assign("/text-to-video");
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
        // Here you can send the customInputs to the server for processing
    } else {
        alert("No custom inputs provided!");
    }
});

// Event listener for the CSV Input card
document.querySelector('.card[data-id="3"]').addEventListener('click', () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.csv';
    fileInput.style.display = 'none';

    document.body.appendChild(fileInput);
    fileInput.click();

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            console.log("CSV File:", file);
            alert(`CSV file uploaded: ${file.name}`);
            // Here you can send this file to the server for processing
        } else {
            alert("No file selected!");
        }
        document.body.removeChild(fileInput);
    });
});
 