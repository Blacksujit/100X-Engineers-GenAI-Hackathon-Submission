 
// Event listener for the Text Input card
document.querySelector('.card[data-id="1"]').addEventListener('click', () => {
    window.location.assign("/text-to-video");
});
// Event listener for the Custom Input card
document.querySelector('.card[data-id="2"]').addEventListener('click', () => {
    window.location.assign("/multi-model-template");
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
