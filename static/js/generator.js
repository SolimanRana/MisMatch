// Shuffle-Function (Fisher-Yates Algorithm)
function shuffleArray(array) {
  const shuffled = [...array]; // Kcreate copy
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// randomize clothing data - randomize when loaded (only one time)
const shuffledClothing = {
  tops: shuffleArray(clothingData.tops),
  bottoms: shuffleArray(clothingData.bottoms),
  footwear: shuffleArray(clothingData.footwear)
};

// current index for each category
let currentIndex = {
  tops: -1,      // -1 = no item yet (box shows "?") 
  bottoms: -1,
  footwear: -1
};

// function to change item 
function changeClothing(category, direction) {
  const items = shuffledClothing[category];
  
  if (!items || items.length === 0) {
    console.error(`No items in this category: ${category}`);
    return;
  }

  // First click: start with index = 0
  if (currentIndex[category] === -1) {
    currentIndex[category] = 0;
  } else {
    // change index (mit wrap-around)
    currentIndex[category] += direction;
    
    // Ring system - end and start are connected
    if (currentIndex[category] < 0) {
      currentIndex[category] = items.length - 1; // to the last item
    } else if (currentIndex[category] >= items.length) {
      currentIndex[category] = 0; // to the first item
    }
  }

  // show image
  displayClothing(category);
}

// function to show image
function displayClothing(category) {
  const box = document.getElementById(`${category}-box`);
  const index = currentIndex[category];

  if (index === -1) {
    // show ?
    box.innerHTML = '<span class="placeholder">?</span>';
  } else {
    // show image from shuffled list
    const item = shuffledClothing[category][index];
    box.innerHTML = `
      <img src="/${item.image_path}" 
           alt="${item.subcategory_name}" 
           class="clothing-image">
    `;
  }
}

// Debugging
console.log('Original Daten:', clothingData);
console.log('Geshuffelte Daten:', shuffledClothing);
console.log('Tops:', shuffledClothing.tops.length);
console.log('Bottoms:', shuffledClothing.bottoms.length);
console.log('Footwear:', shuffledClothing.footwear.length);

// MisMatch Button 
function generateMismatchOutfit() {
  const categories = ['tops', 'bottoms', 'footwear'];
  
  categories.forEach(category => {
    const items = shuffledClothing[category];
    
    if (items && items.length > 0) {
      // choose random index
      const randomIndex = Math.floor(Math.random() * items.length);
      currentIndex[category] = randomIndex;
      
      displayClothing(category);
    }
  });
  
  console.log('MisMatch Outfit generated!');
}

// Save Outfit Function
function saveOutfit() {
  // Check if all items are selected
  if (currentIndex.tops === -1 || currentIndex.bottoms === -1 || currentIndex.footwear === -1) {
    alert('Please select a top, bottom, and footwear first!');
    return;
  }

  const outfitName = prompt('Enter a name for your outfit:', 'My Outfit');
  if (!outfitName) return;

  const outfitData = {
    outfit_name: outfitName,
    top_id: shuffledClothing.tops[currentIndex.tops]._id,
    bottom_id: shuffledClothing.bottoms[currentIndex.bottoms]._id,
    footwear_id: shuffledClothing.footwear[currentIndex.footwear]._id
  };

  fetch('/api/save-outfit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(outfitData)
  })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('Outfit saved!');
        } else {
          alert('Error saving outfit: ' + data.error);
        }
      })
      .catch(error => {
        alert('Error: ' + error);
      });
}