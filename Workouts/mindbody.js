// Click the "More" button on the activity page up to 100 times
for (let i = 0; i < 100; i++) {
    let buttonFound = clickViewMore();
    if (!buttonFound) {
      break; // Exit the loop if the button is not found
    }
    // Add a small delay to allow for content to load (adjust as needed)
    console.log("Iteration:" + (i + 1));
    await new Promise(r => setTimeout(r, 4000)); 
  }
  