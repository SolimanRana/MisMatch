// Function to delete an outfit
async function deleteOutfit(outfitId) {
  // Confirm deletion
  if (!confirm('Are you sure you want to delete this outfit?')) {
    return;
  }

  try {
    const response = await fetch(`/delete-outfit/${outfitId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (response.ok) {
      // Remove the outfit card from the DOM
      const outfitCard = document.querySelector(`[data-outfit-id="${outfitId}"]`);
      if (outfitCard) {
        outfitCard.style.transition = 'opacity 0.3s ease';
        outfitCard.style.opacity = '0';
        
        setTimeout(() => {
          outfitCard.remove();
          
          // Check if there are no more outfits and show empty state
          const outfitsGrid = document.querySelector('.outfits-grid');
          if (outfitsGrid && outfitsGrid.children.length === 0) {
            location.reload(); // Reload to show empty state
          }
        }, 300);
      }

      // Show success message (optional - you can implement a toast notification)
      console.log(data.message);
    } else {
      alert(`Error: ${data.error}`);
    }
  } catch (error) {
    console.error('Error deleting outfit:', error);
    alert('Failed to delete outfit. Please try again.');
  }
}