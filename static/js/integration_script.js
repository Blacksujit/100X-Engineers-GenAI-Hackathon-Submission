document.addEventListener("DOMContentLoaded", () => {
    // Handle Text Input
    const textCard = document.querySelector(".card[data-id='1']");
    textCard.addEventListener("click", async () => {
        const input = prompt("Enter text to process:");
        if (input) {
            try {
                const response = await fetch("/generate_video", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: input }),
                });

                const data = await response.json();
                if (data.video_urls) {
                    alert("Generated Video URLs:\n" + data.video_urls.join("\n"));
                } else {
                    alert("Error: " + data.error);
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred while generating videos.");
            }
        }
    });

    // Handle Custom Input (Data Format: text:data)
    const customCard = document.querySelector(".card[data-id='2']");
    customCard.addEventListener("click", async () => {
        const input = prompt("Enter custom data (e.g., key:value):");
        if (input) {
            try {
                const response = await fetch("/generate_video", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: input }),
                });

                const data = await response.json();
                if (data.video_urls) {
                    alert("Generated Video URLs:\n" + data.video_urls.join("\n"));
                } else {
                    alert("Error: " + data.error);
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred while generating videos.");
            }
        }
    });

    // Handle CSV Input
    const csvCard = document.querySelector(".card[data-id='3']");
    csvCard.addEventListener("click", () => {
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = ".csv";
        fileInput.onchange = async (event) => {
            const file = event.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append("file", file);

                try {
                    const response = await fetch("/upload_csv", {
                        method: "POST",
                        body: formData,
                    });

                    const data = await response.json();
                    if (data.video_urls) {
                        alert("Generated Video URLs:\n" + data.video_urls.join("\n"));
                    } else {
                        alert("Error: " + data.error);
                    }
                } catch (error) {
                    console.error("Error:", error);
                    alert("An error occurred while uploading the file.");
                }
            }
        };
        fileInput.click();
    });
});
