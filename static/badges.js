let notificationQueue = [];
let isNotificationShowing = false; // Flag to prevent concurrent popups
// --- Function to add notifications to the queue ---
export function queueNotifications(badges, levelUpInfo) {
  const newNotifications = [];

  // Add level-up notification if applicable
  if (levelUpInfo) {
      newNotifications.push({ type: 'level', ...levelUpInfo });
  }

  // Add unshown badge notifications
  if (badges && Array.isArray(badges)) {
      badges.filter(b => !b.shown).forEach(badge => {
          newNotifications.push({ type: 'badge', ...badge });
      });
  }

  if (newNotifications.length > 0) {
      notificationQueue = notificationQueue.concat(newNotifications);
      // If no notification is currently showing, start the queue
      if (!isNotificationShowing) {
          showNextNotification();
      }
  }
}


// --- Function to display the next notification in the queue ---
function showNextNotification() {
  if (notificationQueue.length === 0) {
      isNotificationShowing = false; // No more items, reset flag
      return;
  }

  isNotificationShowing = true; // Set flag
  const notification = notificationQueue.shift(); // Get the next item

  const tpl = document.getElementById('badgeTemplate'); // Use the same template
  if (!tpl) {
       console.error("Badge/LevelUp template not found!");
       isNotificationShowing = false; // Reset flag on error
       setTimeout(showNextNotification, 200); // Try next one after delay
       return;
  }
  const popup = tpl.content.firstElementChild.cloneNode(true);

  // --- Configure popup based on type ---
  if (notification.type === 'level') {
      popup.querySelector('img').style.display = 'none'; // Hide image for level up? Or use a default?
      // Alternatively, set a default level-up image source:
      // popup.querySelector('img').src = '/static/level-up-icon.png'; // Example path
      // popup.querySelector('img').alt = 'Level Up!';
      popup.querySelector('.badge-title').textContent = `Level ${notification.level} Reached!`;
      popup.querySelector('.badge-desc').textContent = `Congratulations, you've reached level ${notification.level}!`;

      // Play level-up sound
      try {
          new Audio('/static/levelup.mp3').play();
      } catch (err) { console.error("Error playing levelup sound:", err); }

      // Close button action for level up
      popup.querySelector('#closeBadgePopup').addEventListener('click', () => {
          popup.remove();
          // API call to mark level as shown
          fetch('/update_level_shown', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ level: notification.level })
          })
          .then(res => {
              if (!res.ok) console.error("Failed to update level shown status");
              else console.log(`Level ${notification.level} marked as shown.`);
              // Update local state optimistically (optional, but good practice)
              if (window.currentAppState) {
                  window.currentAppState.highest_level_popup_shown = Math.max(
                      window.currentAppState.highest_level_popup_shown || 0,
                      notification.level
                  );
              }
           })
           .catch(err => console.error("Error in /update_level_shown fetch:", err))
           .finally(() => {
               // Show next notification after a short delay
               isNotificationShowing = false; // Allow next notification to show
               setTimeout(showNextNotification, 200);
           });
      });

  } else if (notification.type === 'badge') {
      popup.querySelector('img').style.display = 'block'; // Ensure image is visible
      popup.querySelector('img').src = notification.image || '/static/default-badge.png'; // Use badge image or a default
      popup.querySelector('img').alt = notification.title;
      popup.querySelector('.badge-title').textContent = notification.title;
      popup.querySelector('.badge-desc').textContent = notification.description;

      // Play badge sound
      try {
          new Audio('/static/badge.mp3').play();
      } catch (err) { console.error("Error playing badge sound:", err); }

      // Close button action for badge
      popup.querySelector('#closeBadgePopup').addEventListener('click', () => {
          popup.remove();
          // API call to mark badge as shown
          fetch('/update_badges', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ badgeIds: [notification.id] })
          })
          .then(res => {
              if (!res.ok) console.error("Failed to update badge shown status");
              else console.log(`Badge ${notification.id} marked as shown.`);
              // Update local badge state (optional)
               if (window.currentAppState && window.currentAppState.badges) {
                  const badgeInState = window.currentAppState.badges.find(b => b.id === notification.id);
                  if (badgeInState) badgeInState.shown = true;
               }
          })
          .catch(err => console.error("Error in /update_badges fetch:", err))
          .finally(() => {
              // Show next notification after a short delay
              isNotificationShowing = false; // Allow next notification to show
              setTimeout(showNextNotification, 200);
          });
      });
  } else {
      console.warn("Unknown notification type:", notification);
       isNotificationShowing = false; // Allow next notification to show
       setTimeout(showNextNotification, 200); // Skip unknown type
       return; // Don't append unknown popup
  }


  document.body.appendChild(popup); // Add the configured popup to the page
}


export function handleBadges(badges) {
  const queue = [...badges.filter(b => !b.shown)]
  if (!queue.length) return

  const showNext = () => {
    const badge = queue.shift()
    if (!badge) return

    const tpl = document.getElementById('badgeTemplate')
    const popup = tpl.content.firstElementChild.cloneNode(true)

    popup.querySelector('img').src = badge.image
    popup.querySelector('img').alt = badge.title
    popup.querySelector('.badge-title').textContent = badge.title
    popup.querySelector('.badge-desc').textContent = badge.description

    document.body.appendChild(popup)

    popup.querySelector('#closeBadgePopup').addEventListener('click', () => {
      popup.remove()
      fetch('/update_badges', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ badgeIds: [badge.id] })
      }).then(() => {
        setTimeout(showNext, 200)
      })
    })
  }

  showNext()
}

export function renderBadgeGallery(badges) {
  const container = document.getElementById('badgesDisplay')
  container.innerHTML = '' // clear old

  badges.forEach(badge => {
    const div = document.createElement('div')
    div.className = 'badge-item'
    div.innerHTML = `
      <img src="${badge.image}" alt="${badge.title}" class="badge-icon" />
      <div class="badge-label">${badge.title}</div>
    `
    container.appendChild(div)
  })
}

function escapeHtml(unsafe) {
  if (unsafe === null || unsafe === undefined) return '';
  return unsafe.toString().replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}