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

const activeClothing = {
  tops: [...shuffledClothing.tops],
  bottoms: [...shuffledClothing.bottoms],
  footwear: [...shuffledClothing.footwear],
}

// current index for each category
let currentIndex = {
  tops: -1,      // -1 = no item yet (box shows "?") 
  bottoms: -1,
  footwear: -1
};

let modalCategory = null;


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

/// function to show image
function displayClothing(category, forcedItem = null) {
  const box = document.getElementById(`${category}-box`);

  let item;

  if (forcedItem) {
    item = forcedItem;
  } else {
    const index = currentIndex[category];
    if (index === -1) {
      box.innerHTML = '<span class="placeholder">?</span>';
      return;
    }
    item = shuffledClothing[category][index];
  }

  const isCustom = item.subcategory === 'custom';

  box.innerHTML = `
    ${isCustom ? `<button class="delete-btn" onclick="deleteClothingItem('${item._id}', '${category}')">🗑️</button>` : ''}
    <img src="/${item.image_path}" class="clothing-image">
  `;
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

    if (!items || items.length === 0) return;

    const randomItem = items[Math.floor(Math.random() * items.length)];

    displayClothing(category, randomItem);

    // optional: Index sauber setzen für Save-Logik
    currentIndex[category] = items.findIndex(
      i => i._id === randomItem._id
    );
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

// Upload Modal Functions (FR-S4)
function openUploadModal() {
  document.getElementById('upload-modal').style.display = 'flex';
}

function closeUploadModal() {
  document.getElementById('upload-modal').style.display = 'none';
  document.getElementById('upload-form').reset();
}

// Handle Upload Form Submit
document.getElementById('upload-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const formData = new FormData();
  formData.append('category', document.getElementById('upload-category').value);
  formData.append('image', document.getElementById('upload-image').files[0]);

  fetch('/api/upload-clothing', {
    method: 'POST',
    body: formData
  })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('Clothing uploaded successfully! Refresh to see it.');
          closeUploadModal();
          location.reload();
        } else {
          alert('Error: ' + data.error);
        }
      })
      .catch(error => {
        alert('Error uploading: ' + error);
      });
});

// Close modal when clicking outside
window.onclick = function(event) {
  const modal = document.getElementById('upload-modal');
  if (event.target === modal) {
    closeUploadModal();
  }
}

// Delete Custom Clothing Item
function deleteClothingItem(itemId, category) {
  if (confirm('Delete this item?')) {
    fetch('/api/delete-clothing/' + itemId, {
      method: 'DELETE'
    })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Item deleted!');
            location.reload();
          } else {
            alert('Error: ' + data.error);
          }
        });
  }
}

// UPDATED: Toggle panel WITHOUT closing others
function togglePanel(category) {
  const panel = document.getElementById(`panel-${category}`);

  // Just toggle this panel - don't close others!
  panel.style.display =
    panel.style.display === 'block' ? 'none' : 'block';

  // Only populate if we're opening it
  if (panel.style.display === 'block') {
    populatePanel(category);
  }
}

function populatePanel(category) {
  const items = clothingData[category];
  const panel = document.getElementById(`panel-${category}`);
  const select = panel.querySelector('select');
  const grid = document.getElementById(`grid-${category}`);

  // COLORS FROM DB
  const colors = [...new Set(
    items.map(i => i.color).filter(Boolean)
  )];

  select.innerHTML = '<option value="all">All colors</option>';
  colors.forEach(c => {
    const o = document.createElement('option');
    o.value = c;
    o.textContent = c;
    select.appendChild(o);
  });

  renderGrid(category, items);
}

function applyColorFilter(category, color) {
  if (color === 'all') {
    activeClothing[category] = [...shuffledClothing[category]];
  } else {
    activeClothing[category] = shuffledClothing[category].filter(
      item => item.color?.toLowerCase() === color.toLowerCase()
    );
  }

  currentIndex[category] = -1;
  displayClothing(category);
  renderGrid(category, activeClothing[category]);
}


function renderGrid(category, items) {
  const grid = document.getElementById(`grid-${category}`);
  grid.innerHTML = '';

  items.forEach(item => {
    const img = document.createElement('img');
    img.src = '/' + item.image_path;

    img.onclick = () => {
      displayClothing(category, item);
      // Don't close the panel anymore - let user keep filtering
    };

    grid.appendChild(img);
  });
}

// ============================================
// HAMBURGER MENU
// ============================================

// Toggle the visibility of the menu when clicked
function toggleHamburgerMenu() {
  const menu = document.getElementById("hamburgerMenu");
  if (menu) {
    menu.classList.toggle("show");
  }
}

// Close the menu if clicking outside of it
document.addEventListener("click", function (event) {
  const menu = document.getElementById("hamburgerMenu");
  const button = document.querySelector(".hamburger-btn");

  if (menu && button && !menu.contains(event.target) && !button.contains(event.target)) {
    menu.classList.remove("show");
  }
});




