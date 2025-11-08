/**
 * Adds the ability to copy a URL to the content by 
 * clicking on buttons with class "copy-link".
 * 
 * An event listener is added to these buttons which copies 
 * the link to the clipboard and then gives a pop-up as 
 * feedback.
 */
const copyLinkItems = document.querySelectorAll('.copy-link');

for (let item of copyLinkItems) {
  let link = item.getAttribute('href');
  item.addEventListener("click", (e) => {
    e.preventDefault();
    let textToCopy = window.location.origin;
    textToCopy += link;
    navigator.clipboard.writeText(textToCopy)
      .then(() => {
        alert('Link copied to clipboard!');
      });
  });
}