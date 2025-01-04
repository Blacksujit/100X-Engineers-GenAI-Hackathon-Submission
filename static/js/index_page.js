 
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
        window.location.assign("/multi-model-template.html");
    } else {
        alert("No custom inputs provided!");
    }
});

// Event listener for the CSV Input card
document.addEventListener('DOMContentLoaded', () => {
    const card = document.querySelector('.card[data-id="3"]');
    console.log("Card element:", card); // Check if the card is selected
    if (card) {
        card.addEventListener('click', () => {
            console.log("CSV Input card clicked!"); // Confirm click event
            try {
                window.location.assign("/csv-to-video");
                console.log("Navigating to /csv-to-video...");
            } catch (error) {
                console.error("Navigation error:", error);
            }
        });
    } else {
        console.error("Card element not found!");
    }
});
